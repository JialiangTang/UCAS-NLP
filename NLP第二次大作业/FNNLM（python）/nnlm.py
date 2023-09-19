import argparse
import math
import time
import random
import numpy as np
# import tensorflow as tf
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior() 

from input_data import TextLoader


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/',
                        help='data directory containing input.txt')
    parser.add_argument('--batch_size', type=int, default=10000,
                        help='minibatch size')
    parser.add_argument('--win_size', type=int, default=5,
                        help='context sequence length')
    parser.add_argument('--hidden_num', type=int, default=128,
                        help='number of hidden layers')
    parser.add_argument('--word_dim', type=int, default=100,
                        help='number of word embedding')
    parser.add_argument('--num_epochs', type=int, default=10,
                        help='number of epochs')
    parser.add_argument('--grad_clip', type=float, default=5.,
                        help='clip gradients at this value')

    args = parser.parse_args()

    data_loader = TextLoader(args.data_dir, args.batch_size, args.win_size)
    args.vocab_size = data_loader.vocab_size

    graph = tf.Graph()
    with graph.as_default():
        input_data = tf.placeholder(tf.int64, [args.batch_size, args.win_size])
        targets = tf.placeholder(tf.int64, [args.batch_size, 1])

        with tf.variable_scope('nnlm' + 'embedding'):
            embeddings = tf.Variable(tf.random_uniform([args.vocab_size, args.word_dim], -1.0, 1.0)) #词向量初始化，均匀分布
            embeddings = tf.nn.l2_normalize(embeddings, 1) #l2标准化

        with tf.variable_scope('nnlm' + 'weight'):# 神经网络参数
            weight_h = tf.Variable(tf.truncated_normal([args.win_size * args.word_dim, args.hidden_num],
                                                       stddev=1.0 / math.sqrt(args.hidden_num)))
            softmax_w = tf.Variable(tf.truncated_normal([args.win_size * args.word_dim, args.vocab_size],
                                                        stddev=1.0 / math.sqrt(args.win_size * args.word_dim)))
            softmax_u = tf.Variable(tf.truncated_normal([args.hidden_num, args.vocab_size],
                                                        stddev=1.0 / math.sqrt(args.hidden_num)))

            b_1 = tf.Variable(tf.random_normal([args.hidden_num]))
            b_2 = tf.Variable(tf.random_normal([args.vocab_size]))

        def infer_output(input_data):
            """
            hidden = tanh(x * H + b_1)
            hidden_output = x * W + hidden * U + b_2
            output = softmax(hidden_output)
            """
            input_data_emb = tf.nn.embedding_lookup(embeddings, input_data)
            input_data_emb = tf.reshape(input_data_emb, [-1, args.win_size * args.word_dim])
            hidden = tf.tanh(tf.matmul(input_data_emb, weight_h)) + b_1
            hidden_output = tf.matmul(hidden, softmax_u) + tf.matmul(input_data_emb, softmax_w) + b_2
            output = tf.nn.softmax(hidden_output)
            return output

        outputs = infer_output(input_data)
        one_hot_targets = tf.one_hot(tf.squeeze(targets), args.vocab_size, 1.0, 0.0)
        loss = -tf.reduce_mean(tf.reduce_sum(tf.log(outputs) * one_hot_targets, 1))
        # Clip grad.
        optimizer = tf.train.AdagradOptimizer(1.0)
        gvs = optimizer.compute_gradients(loss)
        capped_gvs = [(tf.clip_by_value(grad, -args.grad_clip, args.grad_clip), var) for grad, var in gvs]
        optimizer = optimizer.apply_gradients(capped_gvs)

        embeddings_norm = tf.sqrt(tf.reduce_sum(tf.square(embeddings), 1, keep_dims=True))
        normalized_embeddings = embeddings / embeddings_norm #l2正规化
    print("dim of vocabulary is ", data_loader.vocab_size)
    with tf.Session(graph=graph) as sess:
        tf.global_variables_initializer().run()
        for e in range(args.num_epochs):
            data_loader.reset_batch_pointer()
            for b in range(data_loader.num_batches):
                start = time.time()
                x, y = data_loader.next_batch()
                feed = {input_data: x, targets: y}
                train_loss, _ = sess.run([loss, optimizer], feed)
                end = time.time()
                print("{}/{} (epoch {}), train_loss = {:.3f}, time/batch = {:.3f}".format(
                    b, data_loader.num_batches,
                    e, train_loss, end - start))

            np.save('c1998_embeddings.zh', normalized_embeddings.eval()) #词向量保存之处
            

    # normalized_embeddings = normalized_embeddings.array()
    # for i in range(1,21):
    #     similarity = {}
    #     j = random.randint(1,args.vocab_size+1) #随机选一个词
        
    #     for k in range(1,args.vocab_size+1):#遍历词表，计算所有词与它的相似度，存进similarity列表
    #         produce = 0
    #         for p in range(normalized_embeddings[k].shape):
    #             produce += normalized_embeddings[k][p] * normalized_embeddings[j][p]
    #         similarity.update({k:produce})
        
    #     similarity.sort(reverse=True) #降序排列
    #     print("The similar words of "+ data_loader.words[j] + "is:\n")
    #     for l in range(10):
    #         print(data_loader.words[l])



        









if __name__ == '__main__':
    main()
