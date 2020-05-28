
# coding: utf-8

# In[1]:


import pickle
file=open('/home/cel/iit_kgp_event_extraction_model/fixed_length_input/Beng_training_and_vocab_for_argument_15_11.pkl','rb')
train_x=pickle.load(file)
train_y=pickle.load(file)
test_x=pickle.load(file)
test_y=pickle.load(file)
#vocab=pickle.load(file)
file.close()


# In[2]:


vocab=[]
with open('/home/cel/iit_kgp_event_extraction_model/fixed_length_input/bengali_vocab.txt') as f_voc:
    for line in f_voc:
        vocab.append(line.strip())
    f_voc.close()


# In[3]:


train_data_x=[]
train_data_y=[]
test_data_x=[]
test_data_y=[]
train_data_x= train_x
train_data_y= train_y
test_data_x= test_x
test_data_y= test_y


# In[4]:


y_total=train_y+test_y


# In[5]:


#checking unique event types

uniq_entity_type=[]
for k in range(len(y_total)):
    if y_total[k] not in uniq_entity_type:
        uniq_entity_type.append(y_total[k])


# In[6]:


print(len(uniq_entity_type))
print(uniq_entity_type)


# In[7]:


import tensorflow as tf
sess = tf.InteractiveSession()

input_length=9
embed_length=300
no_class=len(uniq_entity_type)
no_hidden=350
learning_rate=0.001
tf.reset_default_graph()
x=tf.placeholder(tf.int32,[None,input_length])
#print(x)
y=tf.placeholder(tf.int32,[None,no_class])
#print(y)

w=tf.Variable(tf.random_normal([2*no_hidden,no_class],stddev=0.35,name='weight_out'),trainable=True)
#print(w)
#w_embedding=tf.Variable(tf.random_normal([len(vocab),embed_length],stddev=0.35,name='weight_embed'),trainable=True)
#print(w_embedding)
#number_of_layers=3

with tf.name_scope("embedding"):
    w_embedding = tf.Variable(tf.constant(0.0, shape=[len(vocab)+1, embed_length]), trainable=True, name="w_embedding")
    embedding_placeholder = tf.placeholder(tf.float32, [len(vocab)+1, embed_length])
    embedding_init = w_embedding.assign(embedding_placeholder)
    embedded_chars = tf.nn.embedding_lookup(w_embedding,x)

#embedded_chars = tf.nn.embedding_lookup(w_embedding,x)

x_rnn=tf.transpose(embedded_chars,[1,0,2])
x_rnn_shape=tf.reshape(x_rnn,[-1,embed_length])
x_shape_rnn=tf.split(x_rnn_shape,input_length,0)
#print(x_shape_rnn)

x_shape_conv=tf.reshape(embedded_chars,[-1,input_length,embed_length,1])
#print(x_shape_conv)

filter_size1=2
filter_size2=3
filter_size3=4
no_of_filter=200

def create_wt(shape):
    return tf.Variable(tf.truncated_normal(shape, stddev=0.05))

def create_bt(size):
    return tf.Variable(tf.constant(0.05, shape=[size]))

def create_conv(ip, no_of_filter, conv_filter_size, no_of_channel):
    wt = create_wt(shape=[conv_filter_size,embed_length,1,no_of_filter])
    b = create_bt(size = no_of_filter)
    layer = tf.nn.conv2d(input = ip, filter= wt, strides =[1,1,1,1], padding='VALID')
    layer_conv=tf.nn.relu(layer+b)
    layer=tf.nn.max_pool(value= layer_conv, ksize= [1,input_length-conv_filter_size+1,1,1],strides=[1,1,1,1],padding='VALID' )
    layer = tf.layers.dropout(layer, rate=0.5, training=True)
    #print(layer)
    return layer

def create_flatten_layer(layer):
    layer=tf.reshape(layer,[-1,no_of_filter*3])
    return layer

def create_fc_layer(ip, no_input, no_output):
    w_fc= create_wt(shape=[no_input,no_output,])
    b_fc= create_bt(no_output)
    layer=tf.matmul(ip,w_fc)+b_fc
    return(layer)


def multirnn(x):
    
    #embedded_chars = tf.nn.embedding_lookup(w_embedding,x)
    #print(embedded_chars)
    #x_unstack = tf.unstack(embedded_chars,input_length, 1)
    #print(x_unstack)
    #x = tf.unstack(x, window_size, 1)
    #cell = tf.contrib.rnn.BasicLSTMCell(no_hidden)
    #x=tf.transpose(embedded_chars,[1,0,2])
    #x=tf.reshape(x,[-1,embed_length])
    #x=tf.split(x,input_length,0)
    #print(x)
    lstm_f_cell=tf.contrib.rnn.BasicLSTMCell(no_hidden,forget_bias=1.0)
    lstm_f_cell_d=tf.nn.rnn_cell.DropoutWrapper(lstm_f_cell, output_keep_prob=0.5)
    lstm_b_cell=tf.contrib.rnn.BasicLSTMCell(no_hidden,forget_bias=1.0)
    lstm_b_cell_d=tf.nn.rnn_cell.DropoutWrapper(lstm_b_cell, output_keep_prob=0.5)
    outputs, _, _=tf.contrib.rnn.static_bidirectional_rnn(lstm_f_cell_d,lstm_b_cell_d,x,dtype=tf.float32)
    #print('output')
    #print(outputs[4])
    #outputs, _, _=tf.contrib.rnn.static_bidirectional_rnn(fw_cell,bw_cell,x_unstack,dtype=tf.float32)
    #cell=tf.contrib.rnn.MultiRNNCell([cell] * number_of_layers)
    #cell = tf.nn.rnn_cell.DropoutWrapper(cell, output_keep_prob=dropout)
    #outputs, _ =  tf.contrib.rnn.static_rnn(cell, x, dtype=tf.float32)
    #outputs, _, _=tf.contrib.rnn.stack_bidirectional_rnn(fw_cell, bw_cell, x, dtype=tf.float32)
    #print('output size')
    #print(outputs[4])
    logit= [tf.matmul(output,w) for output in outputs]
    #print(logit[4])
    return(outputs[4])

output_filter1= create_conv(ip= x_shape_conv, no_of_filter= 200, conv_filter_size= filter_size1, no_of_channel=1)
#print(output_filter1)
output_filter2= create_conv(ip= x_shape_conv, no_of_filter= 200, conv_filter_size= filter_size2, no_of_channel=1)
#print(output_filter2)
output_filter3= create_conv(ip= x_shape_conv, no_of_filter= 200, conv_filter_size= filter_size3, no_of_channel=1)
#print(output_filter3)
final_vector= tf.concat([output_filter1,output_filter2,output_filter3],0)
#print(final_vector)
output_conv_layer=tf.reshape(final_vector,[-1,no_of_filter*3])
#print(output_conv_layer)

output_lstm_layer=multirnn(x_shape_rnn)
#print(output_lstm_layer)
output_concat= tf.concat([output_conv_layer, output_lstm_layer],1)
#print(output_concat)

layer_fc=create_fc_layer(output_concat, no_input = 1300, no_output =len(uniq_entity_type))
#print(layer_fc)
cost=tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits_v2(labels=y,logits=layer_fc))#cost calculation
train=tf.train.AdamOptimizer(learning_rate=learning_rate).minimize(cost)
y_pred= tf.nn.softmax(layer_fc, name='y_pred')
#print(y_pred)
correct_prediction=tf.equal(tf.argmax(y_pred,1),tf.argmax(y,1))
accuracy=tf.reduce_mean(tf.cast(correct_prediction,tf.float32))

predicted_class=tf.argmax(y_pred,1)
#print(predicted_class)
saver = tf.train.Saver()

init = tf.global_variables_initializer()


# In[13]:


import math
import os
import pickle
import numpy as np
MODEL_PATH = os.path.join('/home/cel/iit_kgp_event_extraction_model/bengali_argument_model/50/','my-model.ckpt-50')
#import tensorflow as tf


import sys
from importlib import reload
reload(sys)
#sys.setdefaultencoding('utf8')

#tf.reset_default_graph()


output_path='/home/cel/iit_kgp_event_extraction_model/output/test_argument_output/'
path='/home/cel/iit_kgp_event_extraction_model/input_test_files/test_file_normalized/'
saver = tf.train.Saver()
with tf.Session() as sess:
    saver.restore(sess, MODEL_PATH)
    for filename  in os.listdir(path):
        fullPath = os.path.join(path, filename)
        if os.path.isfile(fullPath):
            test_file=open(fullPath,'rb')
            test_x=pickle.load(test_file)
            #test_y=pickle.load(test_file)
            #test_z=pickle.load(test_file)
            word_list=pickle.load(test_file,encoding='utf8')
            x_test=test_x
            #y_test=test_z
            acc=0
            ptr=1
            bs=0
            #test_window_size=len(x_test)
            #test_x=np.reshape(x_test,[batch_size,test_window_size,embed_length])
            #test_y=np.reshape(y_test,[batch_size,test_window_size,no_class])
            #acc=sess.run(accuracy,feed_dict={x:test_x,y:test_y})
            tagset=[]
            batch_size=1
            n_batch = int(math.ceil(len(x_test) / batch_size))
            print(n_batch)
        
        
            
            
            while ptr <= n_batch:
                if ptr*batch_size < len(x_test):
                    ip=x_test[bs:bs+batch_size]
                else:
                    ip =x_test[bs:]
                bs+=batch_size
                ip=np.reshape(ip,[batch_size,input_length])
                #op=np.reshape(op,[batch_size,no_class])
                ptr+=1
                pred=sess.run(predicted_class,feed_dict={x:ip})
                for p1 in pred:
                    tagset.append(p1)
                    #print 'p1 = ', p1
                    #for p2 in p1:
                    #print 'p2 = ', np.asarray(softmax(p2))
               
                #acc+=sess.run(accuracy,feed_dict={x:ip,y:op})
            #print (acc/ptr), len(tagset)
            #print(tagset)
            f_out=open(output_path+filename.replace('pkl','txt'),'w+')
            t=0
            while t<len(tagset):
                f_out.write(str(word_list[t])+'   '+str(uniq_entity_type[tagset[t]])+'\n')
                t+=1
            f_out.close()

