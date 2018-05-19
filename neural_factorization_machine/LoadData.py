'''
Utilities for Loading data.
The input data file follows the same input for LibFM: http://www.libfm.org/libfm-1.42.manual.pdf

@author:
Xiangnan He (xiangnanhe@gmail.com)
Lizi Liao (liaolizi.llz@gmail.com)

@references:
'''
import numpy as np
import numpy.random as random
import copy
import os

class LoadData(object):
    '''given the path of data, return the data format for DeepFM
    :param path
    return:
    Train_data: a dictionary, 'Y' refers to a list of y values; 'X' refers to a list of features_M dimension vectors with 0 or 1 entries
    Test_data: same as Train_data
    Validation_data: same as Train_data
    '''

    # Three files are needed in the path
    def __init__(self, path, dataset, loss_type, feature_length):
        self.path = path + dataset + "/"
        self.trainfile = self.path + dataset +".train.libfm"
        self.testfile = self.path + dataset + ".test.libfm"
        self.validationfile = self.path + dataset + ".test.libfm"
        # self.negativefile = self.path + dataset + ".neg"
        self.features_M = self.map_features(feature_length)
        # self.dict_neg = self.read_neg(self.negativefile)
        self.Train_data, self.Validation_data, self.Test_data = self.construct_data( loss_type )

    def read_neg(self, file):
        data_neg = {}
        with open(file, "r") as f:
            lines = f.readlines()
            idx = [i for i in range(len(lines))]
            random.shuffle(idx)
            for i in idx:
                line = lines[i]
                items = line.split(' ')
                data = {}
                data['Y'] = float(items[0])
                data['X'] = [ self.features[item.split(":")[0]] for item in items[1:]]
                data['C'] = [ float(item.split(":")[1]) for item in items[1:]]
                user = data['X'][0]

                if user in data_neg:
                    data_neg[user].append(data)
                else:
                    data_neg[user] = [data]
        return data_neg

    def neg_sampling(self, data, n=0):
        if n == 0:
            return data
        data_expend = copy.deepcopy(data)
        for user in self.dict_neg.keys():
            for i in range(n):
                d = self.dict_neg[user][random.randint(len(self.dict_neg[user]))]
                data_expend['X'].append(d['X'])
                data_expend['Y'].append(d['Y'])
                data_expend['C'].append(d['C'])
        return data_expend

    def map_features(self, length=None): # map the feature entries in all files, kept in self.features dictionary
        if length is not None:
            self.features = {str(i):i for i in range(length)}
        else:
            self.features = {}
            self.read_features(self.trainfile)
            self.read_features(self.testfile)
            self.read_features(self.validationfile)
            # self.read_features(self.negativefile)
        #print("features_M:", len(self.features))
        return  len(self.features)

    def read_features(self, file): # read a feature file
        f = open( file )
        line = f.readline()
        i = len(self.features)
        while line:
            items = line.strip().split(' ')
            for item in items[1:]:
                item = item.split(":")[0]
                if item not in self.features:
                    self.features[ item ] = i
                    i += 1
            line = f.readline()
        f.close()

    def construct_data(self, loss_type):
        X_, C_, Y_ , Y_for_logloss= self.read_data(self.trainfile)
        if loss_type == 'log_loss':
            Train_data = self.construct_dataset(X_, C_, Y_for_logloss)
        else:
            Train_data = self.construct_dataset(X_, C_, Y_)
        print("# of training:" , len(Y_))

        X_, C_, Y_ , Y_for_logloss= self.read_data(self.validationfile)
        if loss_type == 'log_loss':
            Validation_data = self.construct_dataset(X_, C_, Y_for_logloss)
        else:
            Validation_data = self.construct_dataset(X_, C_, Y_)
        print("# of validation:", len(Y_))

        X_, C_, Y_, Y_for_logloss = self.read_data(self.testfile)
        if loss_type == 'log_loss':
            Test_data = self.construct_dataset(X_, C_, Y_for_logloss)
        else:
            Test_data = self.construct_dataset(X_, C_, Y_)
        print("# of test:", len(Y_))

        return Train_data,  Validation_data,  Test_data

    def read_data(self, file):
        # read a data file. For a row, the first column goes into Y_;
        # the other columns become a row in X_ and entries are maped to indexs in self.features
        f = open( file )
        X_ = []
        C_ = []
        Y_ = []
        Y_for_logloss = []
        line = f.readline()
        while line:
            items = line.strip().split(' ')
            Y_.append( 1.0*float(items[0]) )

            if float(items[0]) > 0:# > 0 as 1; others as 0
                v = 1.0
            else:
                v = 0.0
            Y_for_logloss.append( v )

            X_.append( [ self.features[item.split(":")[0]] for item in items[1:]] )

            # C = []
            # for item in items[1:]:
            #     if item.split(":")[0] == '3000':
            #         print(item)
            #         C.append(0.0)
            #     else:
            #         C.append(float(item.split(":")[1]))
            #
            # C_.append(C)

            C_.append( [ float(item.split(":")[1]) for item in items[1:]])
            line = f.readline()
        f.close()

        return X_, C_, Y_, Y_for_logloss

    def construct_dataset(self, X_, C_, Y_):
        Data_Dic = {}
        X_lens = [ len(line) for line in X_]
        indexs = np.argsort(X_lens)
        Data_Dic['Y'] = [ Y_[i] for i in indexs]
        Data_Dic['C'] = [ C_[i] for i in indexs]
        Data_Dic['X'] = [ X_[i] for i in indexs]
        return Data_Dic

    def truncate_features(self):
        """
        Make sure each feature vector is of the same length
        """
        num_variable = len(self.Train_data['X'][0])
        for i in xrange(len(self.Train_data['X'])):
            num_variable = min([num_variable, len(self.Train_data['X'][i])])
        # truncate train, validation and test
        for i in xrange(len(self.Train_data['X'])):
            self.Train_data['X'][i] = self.Train_data['X'][i][0:num_variable]
        for i in xrange(len(self.Validation_data['X'])):
            self.Validation_data['X'][i] = self.Validation_data['X'][i][0:num_variable]
        for i in xrange(len(self.Test_data['X'])):
            self.Test_data['X'][i] = self.Test_data['X'][i][0:num_variable]
        return num_variable
