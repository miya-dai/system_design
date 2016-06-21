import numpy as np
import pandas as pd
import sys
from PEIOPT_for_loop import *
import csv
import time

x_all = pd.read_csv("./../x_all.csv", header=None)
y_all = pd.read_csv("./../y_all.csv", header=None)
cas_data = pd.read_csv("./../sum_log.csv")
counter_i = 1

csv_title_list = ["trial","cas_number","pred_value","real_value","error_value"]

f = open('PEIOPT_process_10_200.csv', 'w')
writer = csv.writer(f, lineterminator='\n')
writer.writerow(csv_title_list)

sampler = np.random.permutation(len(x_all))

learn_x = x_all.take(sampler[:10])
learn_y = y_all.take(sampler[:10])
cas_source = (cas_data.ix[:,1]).take(sampler[10:])
cas_source = list(cas_source.values.flatten())
#
test_x = x_all.take(sampler[10:])
test_y = y_all.take(sampler[10:])
#

#こっからループ
for i in range(200):
    learn_x.to_csv("./x_10_1.csv", index=False, header=False)
    learn_y.to_csv("./y_10_1.csv", index=False, header=False)
    test_x.to_csv("./xeval_10_1.csv", index=False, header=False)
    test_y.to_csv("./yeval_10_1.csv", index=False, header=False)


    #最適化手法本体

    # データロード
    X = np.loadtxt("./x_10_1.csv",delimiter=",")
    X = X.astype(np.float64)#設計変数
    ycsv = pd.read_csv("./y_10_1.csv", header=None)
    add_rand = np.random.rand(len(ycsv)) * np.random.rand(len(ycsv)) * 0.1
    for i in range(len(ycsv)):
        ycsv.ix[i,0] = ycsv.ix[i,0] + add_rand[i]
    y = ycsv.as_matrix()
    y = y.astype(np.float64)#特性
    boundcsv = np.loadtxt("bound.csv",delimiter=",")#設計変数のレンジ
    yinfcsv = np.loadtxt("yinf.csv",delimiter=",")#各特性に対する要求
    option = pd.read_csv("option.csv", header=None)#option

    #二次元配列に統一
    if boundcsv.ndim == 1:
        boundcsv = boundcsv[:,np.newaxis]
        X = X[:,np.newaxis]
    if yinfcsv.ndim == 1:
        yinfcsv = yinfcsv[:,np.newaxis]

    #boundとyinfをリストの形にする
    bounds = []
    yinf = []
    for var in range(0, boundcsv.shape[1]):
        bounds.append([boundcsv[0,var],boundcsv[1,var]])
    for var in range(0, yinfcsv.shape[1]):
        yinf.append([yinfcsv[0,var],yinfcsv[1,var],yinfcsv[2,var]])

    optfunc_first = []
    Xselec = []
    theta = []
    result = []
    # 任意の数の候補を選択するまでループ
    for i in range(0,int(option[1][1])):
        # GPモデルの構築
        if i == 0: #最初は全ての特性値に対してモデルを構築する
            gp_list = []#各特性ごとに作成したGPモデルを格納するリスト
            for obj in range(0,len(yinf)):
                gp = GaussianProcess(thetaL = 0.0000001, thetaU = 100)
                Xdb = X[np.isnan(y[:,obj]) == False, :]#yが欠損値の場合は無視
                ydb = y[np.isnan(y[:,obj]) == False, obj]#yが欠損値の場合は無視
                gp.fit(Xdb, ydb)
                gp_list.append(gp)

        else:#二回目以降は最適化する特性のみのモデルを再構築する。
            gp = GaussianProcess(theta0 = theta)
            Xdb = X[np.isnan(y[:,optfunc_first.optobj]) == False, :]#yが欠損値の場合は無視
            ydb = y[np.isnan(y[:,optfunc_first.optobj]) == False, optfunc_first.optobj]#yが欠損値の場合は無視

            #ダミーデータをデータベースに追加
            Xdb = np.r_[Xdb, Xselec]
            ydb = np.r_[ydb[:,np.newaxis], optfunc_first.CL[int(option[1][2])]*np.ones([i,1])]

            gp.fit(Xdb, ydb)
            gp_list[optfunc_first.optobj] = gp

        # DEの準備
        optfunc = Opt_func(y = y, model = gp_list, yinfdata = yinf, option = option)#最適化する関数を含むオブジェクトを作成  
        if i == 0:
            #最初に作成したモデルは保存しておく
            gp_list_first = gp_list.copy()
            optfunc_first = Opt_func(y = y, model = gp_list_first, yinfdata = yinf, option = option)
            #2回目以降はこのハイパーパラメータを用いてモデルを構築する
            theta = gp_list[optfunc_first.optobj].theta_

        # DE
        if int(option[1][4]) == 0:
            if int(option[1][0]) == 0:
                de_result = differential_evolution(optfunc.P, bounds)#Pで選択
            elif int(option[1][0]) == 1:
                de_result = differential_evolution(optfunc.EI, bounds)#EIで選択
            elif int(option[1][0]) == 2:
                de_result = differential_evolution(optfunc.Y, bounds)#予測値で選択

        elif int(option[1][4]) == 1:
            #評価を行うリストを読み込み
            Xeval = np.loadtxt("./xeval_10_1.csv",delimiter=",")
            Xeval = Xeval.astype(np.float64)

            #評価
            if int(option[1][0]) == 0:
                eval = optfunc.P(Xeval)#Pで選択
            elif int(option[1][0]) == 1:
                eval = optfunc.EI(Xeval)#EIで選択
            elif int(option[1][0]) == 2:
                eval = optfunc.Y(Xeval)#予測値で選択

            #候補の選択
            de_result = result_cont(Xeval[eval.argmin(),:],eval.argmin())

        #選択された候補を格納
        if i == 0:
            Xselec = de_result.x[:,np.newaxis].T
        else:
            Xselec = np.r_[Xselec, de_result.x[:,np.newaxis].T]

        #出力用のデータフレームを作成
        result_temp = pd.DataFrame(de_result.x.T).T#Xを格納
        result_temp[result_temp.shape[1]] = de_result.message#DEの最適化の終了メッセージを格納

        #最初に作成したモデル（ダミーデータを含まない）で評価を行い、その評価値を格納する
        if int(option[1][0]) == 0:
            eve = optfunc_first.P(de_result.x[:,np.newaxis].T)
            result_of_y_pred = optfunc_first.ypred
        elif int(option[1][0]) == 1:
            eve = optfunc_first.EI(de_result.x[:,np.newaxis].T)
            result_of_y_pred = optfunc_first.ypred
        elif int(option[1][0]) == 2:
            eve = optfunc_first.Y(de_result.x[:,np.newaxis].T)
            if optfunc_first.optdirection < 0:
                eve = -eve

        result_temp[result_temp.shape[1]] = -eve
        result_temp[result_temp.shape[1]] = "id"
        result_temp[result_temp.shape[1]] = '-' if (int(option[1][4]) == 0) else de_result.id


        #出力用のデータフレームを更新
        if i == 0:
            result = result_temp
        else:
            result = pd.concat([result,result_temp], axis=0)
    y_pred_value = pd.Series(result_of_y_pred[0])
#    print(y_pred_value)
    result = pd.concat([result,y_pred_value], axis=1)
    #print("succeed")
#    print(cas_source[de_result.id])

    y_eval = pd.read_csv("./yeval_10_1.csv", header=None)
    y_real_value = y_eval.ix[de_result.id,0]

    write_list = []
    write_list.append(counter_i)
    counter_i += 1
    print(len(learn_x))
#    print(de_result.id)
    write_list.append(cas_source[de_result.id])
    write_list.append(result_of_y_pred[0][0])
    write_list.append(y_eval.ix[de_result.id,0])
#    print(y_eval.ix[de_result.id,0])
    error_value = abs(result_of_y_pred[0][0] - y_eval.ix[de_result.id,0])
    write_list.append(error_value)
    writer.writerow(write_list)

    learn_x = learn_x.append(test_x.iloc[de_result.id,:])
    learn_y = learn_y.append(test_y.iloc[de_result.id,:])
    if de_result.id == 0:
        test_x = test_x.iloc[1:]
        test_y = test_y.iloc[1:]
    else:
        test_x = pd.concat([test_x.iloc[0:de_result.id -1 ], test_x.iloc[de_result.id:]])
        test_y = pd.concat([test_y.iloc[0:de_result.id -1 ], test_y.iloc[de_result.id:]])
    del cas_source[de_result.id]
#    print(len(cas_source))
#    print(learn_x)
f.close()
		#結果の出力
#result.to_csv("result_cand_1_EI.csv", index=False, header=False)

