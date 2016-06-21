#Xに分子のIDを追加できるように改良（Xの1列目を無視する）
# H.Uratani 2016/6/20


import numpy as np
from scipy import stats
from scipy.optimize import differential_evolution
from sklearn.gaussian_process import GaussianProcess
import pandas as pd

class Opt_func:
    """
    最適化する関数
    func = 0 なら　P
    func = 1 なら　EI
    """ 
    # Standard normal distribution functions
    phi = stats.distributions.norm().pdf
    PHI = stats.distributions.norm().cdf

    def __init__(self, y, model, yinfdata, option):# コンストラクタ
        self.gp_list = model#特性ごとのGPモデルのリスト
        self.yinf = yinfdata#yの制約条件等
        self.ydb = y#yのデータベース
        self.option = option#optionファイル
        
        #最適化する目的変数を決める
        for obj in range(0,len(yinf)):
            if np.abs(yinf[obj][0]) > 0.5:
                self.optobj = obj
                break
        
        #最適化の方向を決める
        if self.yinf[self.optobj][0] > 0:
            self.optdirection = 1;
        else:
            self.optdirection = -1;
                 
        self.optY = self.optYvalue()#現在の最適値
        self.CL = self.CLvalue()#複数選択に用いる偽の特性値
        
    #評価値Pの計算
    def P(self, X):
        ypred_list = []
        sigma_list = []
        
        #各目的変数に対してGPモデルで予測
        for obj in range(0,len(yinf)):
            gp = self.gp_list[obj]
            y_pred, MSE = gp.predict(X, eval_MSE=True)
            sigma = np.sqrt(MSE)
            ypred_list.append(y_pred)
            sigma_list.append(sigma)
        
        #制約条件なしで最適値を更新する確率を求める
        y_pred_opt = ypred_list[self.optobj]
        sigma_opt = sigma_list[self.optobj]
        if self.optdirection > 0:
            p = self.PHI( (y_pred_opt - self.optY - self.option[1][3]) / sigma_opt)
        else:
            p = self.PHI( (self.optY - self.option[1][3] - y_pred_opt) / sigma_opt)            
        
        #制約条件を満たす確率をかける
        for obj in range(0,len(yinf)):
            if not obj == self.optobj:
                y_pred_const = ypred_list[obj]
                sigma_const = sigma_list[obj]
                p = p * (self.PHI( (y_pred_const - yinf[obj][1]) / sigma_const) - self.PHI((y_pred_const - yinf[obj][2]) / sigma_const))
        
        self.ypred = ypred_list
        self.sigma = sigma_list
        self.p = p
        
        return -p
    
    #最適値の更新幅の期待値
    def EI(self,X):
        ypred_list = []
        sigma_list = []
        
        #各目的変数に対してGPモデルで予測
        for obj in range(0,len(yinf)):
            gp = self.gp_list[obj]
            y_pred, MSE = gp.predict(X, eval_MSE=True)
            sigma = np.sqrt(MSE)
            ypred_list.append(y_pred)
            sigma_list.append(sigma)
        
        
        y_pred_opt = ypred_list[self.optobj]
        sigma_opt = sigma_list[self.optobj]
        
        #最大化の時は最小化問題に直す
        if self.optdirection == 1:
            y_pred_opt = - y_pred_opt
            optY_ei = - self.optY
        else:
            optY_ei = self.optY
        
        #制約条件なしで場合の最適値の更新幅の期待値
        if np.isinf(optY_ei) == False:
            ei = (optY_ei - y_pred_opt)*self.PHI( (optY_ei - y_pred_opt) / sigma_opt) + sigma_opt * self.phi( (optY_ei - y_pred_opt) / sigma_opt)
        else:
            ei = 1
        
        #制約条件を満たす確率をかける
        for obj in range(0,len(yinf)):
            if not obj == self.optobj:
                y_pred_const = ypred_list[obj]
                sigma_const = sigma_list[obj]
                ei = ei * (self.PHI( (y_pred_const - yinf[obj][1]) / sigma_const) - self.PHI((y_pred_const - yinf[obj][2]) / sigma_const))
        
        self.ypred = ypred_list
        self.sigma = sigma_list
        self.ei = ei
        
        return -ei
        
    #予測値のみから選択
    def Y(self,X):
        ypred_list = []
        sigma_list = []
        
        #各目的変数に対してGPモデルで予測
        for obj in range(0,len(yinf)):
            gp = self.gp_list[obj]
            y_pred, MSE = gp.predict(X, eval_MSE=True)
            sigma = np.sqrt(MSE)
            ypred_list.append(y_pred)
            sigma_list.append(sigma)
        
        #制約条件を満たさない候補が選ばれないように代入する無限大を選択
        y = ypred_list[self.optobj]
        if self.optdirection == 1:
            outvalue = -np.inf
        else:
            outvalue = np.inf
        
        #予測値が制約条件を満たさない場合はNGなので無限大を代入
        for obj in range(0,len(yinf)):
            if not obj == self.optobj:
                if ypred_list[obj] < yinf[obj][1]:
                    y = outvalue
                if ypred_list[obj] > yinf[obj][2]:
                    y = outvalue        
        
        #最小化問題になるように出力
        if self.optdirection == 1:
            return -y
        else:
            return y
        
    #トレーニングデータ中の最適値を計算
    def optYvalue(self):
        yok = self.ydb[:,self.optobj]#最適化を行う特性を抽出
            
        #制約条件を満たさない候補には無限大を代入
        for obj in range(0,len(yinf)):
            if not obj == self.optobj:
                yok[y[:,obj] < yinf[obj][1]] = - self.optdirection * np.inf
                yok[y[:,obj] > yinf[obj][2]] = - self.optdirection * np.inf
            
        #残った候補から最も良い特性値を選ぶ
        if self.optdirection > 0:
            yopt = np.max(yok)
        else:
            yopt = np.min(yok)
            
        return yopt
        
    #複数選択に用いる偽の値を格納したリストの作成
    #0:最適値から最も遠い候補
    #1：データの中央値
    #2:最適値に最も近い候補
    #となるようにリストを作成する
    def CLvalue(self):
        ymax = np.max(self.ydb[:,self.optobj])
        ymin = np.min(self.ydb[:,self.optobj])
        ymid = np.median(self.ydb[:,self.optobj])
        
        CL = []
        if self.optdirection == 1:
            CL.append(ymin)
            CL.append(ymid)
            CL.append(ymax)
        else:
            CL.append(ymax)
            CL.append(ymid)
            CL.append(ymin)
            
        return CL
        
class result_cont:
    def __init__(self, x, id):# コンストラクタ
        self.x = x;
        self.id = id;
        self.message = "List is used"
    """
    結果の格納
    """ 
    
"""
最適化手法本体
""" 
# データロード
X = np.loadtxt("X.csv",delimiter=",")
X = X.astype(np.float64)#設計変数
ycsv = pd.read_csv("y.csv", header=None)
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
#Xの1列目はIDなので無視する
X = np.delete(X, 0, 1)

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
        Xeval = np.loadtxt("Xeval.csv",delimiter=",")
        Xeval = Xeval.astype(np.float64)
        #Xevalの1列目はIDなので無視する
        Xeval = np.delete(Xeval, 0, 1)
    
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
    elif int(option[1][0]) == 1:
        eve = optfunc_first.EI(de_result.x[:,np.newaxis].T)
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
    
#結果の出力
result.to_csv("result.csv")