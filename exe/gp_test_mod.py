import numpy as np
from scipy import stats
from scipy.optimize import differential_evolution
from sklearn.gaussian_process import GaussianProcess

# Standard normal distribution functions
phi = stats.distributions.norm().pdf
PHI = stats.distributions.norm().cdf

class Opt_func:
    """
    最適化する関数
    func = 0 なら　P
    func = 1 なら　EI
    """ 

    def __init__(self, model, yinfdata):# コンストラクタ
        self.name = ""
        
    def P(X, model, yinf):
        p = 0
        return p
    
    def EI(X, model, yinf):
        ie = 0
        return ie    

# データロード
X = np.loadtxt("x_20.csv",delimiter=",")
y = np.loadtxt("y_logS_20.csv",delimiter=",")
boundcsv = np.loadtxt("bound.csv",delimiter=",")
yinfcsv = np.loadtxt("yinf_test.csv",delimiter=",")

# GPモデルの構築
gp = GaussianProcess(thetaL = 0.0000001, thetaU = 100)
gp.fit(X, y)

if yinfcsv.ndim == 1:
    yinfcsv = yinfcsv[:,np.newaxis]
# DEの準備
bounds = []
yinf = []

for var in range(0, boundcsv.shape[1]):
    bounds.append([boundcsv[0,var],boundcsv[1,var]])
for var in range(0, yinfcsv.shape[1]):
    yinf.append([yinfcsv[0,var],yinfcsv[1,var]])
P = Opt_func(model = gp, yinfdata = yinf)
    
# DE
de_result = differential_evolution(P, bounds)
    

y_true = g(xx)
y_pred, MSE = gp.predict(xx, eval_MSE=True)
sigma = np.sqrt(MSE)
y_true = y_true.reshape((res, res))
y_pred = y_pred.reshape((res, res))
sigma = sigma.reshape((res, res))
k = PHIinv(.975)

# Plot the probabilistic classification iso-values using the Gaussian property
# of the prediction
fig = pl.figure(1)
ax = fig.add_subplot(111)
ax.axes.set_aspect('equal')
pl.xticks([])
pl.yticks([])
ax.set_xticklabels([])
ax.set_yticklabels([])
pl.xlabel('$x_1$')
pl.ylabel('$x_2$')

cax = pl.imshow(np.flipud(PHI(- y_pred / sigma)), cmap=cm.gray_r, alpha=0.8,
                extent=(- lim, lim, - lim, lim))
norm = pl.matplotlib.colors.Normalize(vmin=0., vmax=0.9)
cb = pl.colorbar(cax, ticks=[0., 0.2, 0.4, 0.6, 0.8, 1.], norm=norm)
cb.set_label('${\\rm \mathbb{P}}\left[\widehat{G}(\mathbf{x}) \leq 0\\right]$')

pl.plot(X[y <= 0, 0], X[y <= 0, 1], 'r.', markersize=12)

pl.plot(X[y > 0, 0], X[y > 0, 1], 'b.', markersize=12)

cs = pl.contour(x1, x2, y_true, [0.], colors='k', linestyles='dashdot')

cs = pl.contour(x1, x2, PHI(- y_pred / sigma), [0.025], colors='b',
                linestyles='solid')
pl.clabel(cs, fontsize=11)

cs = pl.contour(x1, x2, PHI(- y_pred / sigma), [0.5], colors='k',
                linestyles='dashed')
pl.clabel(cs, fontsize=11)

cs = pl.contour(x1, x2, PHI(- y_pred / sigma), [0.975], colors='r',
                linestyles='solid')
pl.clabel(cs, fontsize=11)

pl.show()