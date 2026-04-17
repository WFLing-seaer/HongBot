from collections.abc import Callable

import numpy as np
from scipy import stats

if __package__:
    from .nameutil import Names
else:
    from nameutil import Names

rsgs: Names[Callable[[int], np.ndarray]] = Names()
rngs: Names[Callable[[], float]] = Names()


@rsgs.named(
    "n",
    "正态",
    "正态分布",
    "gauss",
    "gaussian",
    "高斯",
    "高斯分布",
    "b",
    "2",
    "binom",
    "二项",
    "二项分布",
    "poisson",
    "泊松",
    "泊松分布",
    "超几何",
    "超几何分布",
)
def rsg_norm(x_segments):
    """
    正态 μ=0 σ=1
    -3.2905267315 ~ 3.2905267315 (CDF 0.999)
    """
    domain_min = -3.2905267315
    domain_max = 3.2905267315
    p_domain = 0.999

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.norm.cdf(points, loc=0, scale=1)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("t", "学生", "学生分布", "t分布", "t-分布")
def rsg_t(x_segments):
    """
    T df=4
    -8.6103015813 ~ 8.6103015813 (CDF 0.999)
    """
    domain_min = -8.6103015813
    domain_max = 8.6103015813
    p_domain = 0.999
    df = 4

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.t.cdf(points, df=df)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named(
    "x",
    "x2",
    "x^2",
    "x²",
    "χ",
    "χ2",
    "χ^2",
    "χ²",
    "c2",
    "c^2",
    "c²",
    "卡方",
    "卡方分布",
    "σ",
    "s",
    "西格马",
    "西格马分布",
    "希格玛",
    "希格玛分布",
    "西格玛",
    "西格玛分布",
)
def rsg_chi2(x_segments):
    """
    卡方 df=4
    0 ~ 18.4668269 (CDF 0.999)
    """
    domain_min = 0
    domain_max = 18.4668269
    p_domain = 0.999
    df = 4

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.chi2.cdf(points, df=df)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("f", "f分布", "f-分布")
def rsg_f(x_segments):
    """
    F df1=4 df2=4
    0 ~ 15.9770248525577 (CDF 0.99)
    """
    domain_min = 0
    domain_max = 15.9770248525577
    p_domain = 0.99
    df1, df2 = 4, 4

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.f.cdf(points, df1, df2)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("e", "exp", "指数", "指数分布", "geo", "geometric", "几何", "几何分布")
def rsg_exp(x_segments):
    """
    指数 λ=1
    0 ~ 6.9077552789821 (CDF 0.999)
    """
    domain_min = 0
    domain_max = 6.9077552789821
    p_domain = 0.999
    scale = 1  # λ=1时，scale=1

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.expon.cdf(points, scale=scale)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("c", "cauchy", "柯西", "柯西分布")
def rsg_cauchy(x_segments):
    """
    柯西 med=0 scale=1
    -6.313751514675 ~ 6.313751514675 (CDF 0.9)
    """
    domain_min = -6.313751514675
    domain_max = 6.313751514675
    p_domain = 0.9
    loc, scale = 0, 1

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.cauchy.cdf(points, loc=loc, scale=scale)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("w", "weibull", "威布尔", "威布尔分布", "韦布尔", "韦布尔分布", "韦伯", "韦伯分布", "韦氏分布")
def rsg_weibull(x_segments):
    """
    威布尔 shape=5 scale=1
    0 ~ 1.471863002149 (CDF 0.999)
    """
    domain_min = 0
    domain_max = 1.471863002149
    p_domain = 0.999
    c, scale = 5, 1  # shape=5

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.weibull_min.cdf(points, c, scale=scale)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("g", "γ", "gamma", "伽马", "伽马分布", "p", "pascal", "帕斯卡", "帕斯卡分布")
def rsg_gamma(x_segments):
    """
    伽马 α=3 β=2
    0 ~ 22.45774448485 (CDF 0.999)
    """
    domain_min = 0
    domain_max = 22.45774448485
    p_domain = 0.999
    alpha, beta = 3, 2

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.gamma.cdf(points, a=alpha, scale=1 / beta)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("β", "beta", "贝塔", "贝塔分布", "β分布", "b分布", "b-分布")
def rsg_beta(x_segments):
    """
    β α=2 β=2
    0 ~ 1 (CDF 1.0)
    """
    domain_min = 0
    domain_max = 1
    p_domain = 1.0
    a, b = 2, 2

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.beta.cdf(points, a, b)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("log", "ln", "logn", "lognorm", "对数正态", "对数正态分布")
def rsg_lognorm(x_segments):
    """
    对数正态 μ=0 σ=1
    0 ~ 10.2404736563121 (CDF 0.99)
    """
    domain_min = 0
    domain_max = 10.2404736563121
    p_domain = 0.99
    mu, sigma = 0, 1

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.lognorm.cdf(points, s=sigma, scale=np.exp(mu))
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named("logistic", "逻辑", "逻辑分布")
def rsg_logistic(x_segments):
    """
    逻辑 μ=5 scale=2
    -15.586609649449 ~ 15.586609649449 (CDF 0.99)
    """
    domain_min = -15.586609649449
    domain_max = 15.586609649449
    p_domain = 0.99
    loc, scale = 5, 2

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.logistic.cdf(points, loc=loc, scale=scale)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rsgs.named(
    "l",
    "lap",
    "laplace",
    "拉普拉斯",
    "拉普拉斯分布",
    "双指数",
    "双指数分布",
)
def rsg_laplace(x_segments):
    """
    拉普拉斯 μ=0 b=1
    -4.60517018599 ~ 4.60517018599 (CDF 0.99)
    """
    domain_min = -4.60517018599
    domain_max = 4.60517018599
    p_domain = 0.99
    loc, scale = 0, 1

    points = np.linspace(domain_min, domain_max, x_segments + 1)
    cdf_vals = stats.laplace.cdf(points, loc=loc, scale=scale)
    probs = np.diff(cdf_vals)
    probs = probs / p_domain

    return probs


@rngs.named(
    "n",
    "正态",
    "正态分布",
    "gauss",
    "gaussian",
    "高斯",
    "高斯分布",
    "b",
    "2",
    "binom",
    "二项",
    "二项分布",
    "poisson",
    "泊松",
    "泊松分布",
    "超几何",
    "超几何分布",
)
def rng_norm():
    domain_min = -3.2905267315
    domain_max = 3.2905267315
    while True:
        val = stats.norm.rvs(loc=0, scale=1)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("t", "t分布", "学生", "学生分布", "t-分布", "t-分布")
def rng_t():
    domain_min = -8.6103015813
    domain_max = 8.6103015813
    df = 4
    while True:
        val = stats.t.rvs(df=df)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named(
    "x",
    "x2",
    "x^2",
    "x²",
    "χ",
    "χ2",
    "χ^2",
    "χ²",
    "c2",
    "c^2",
    "c²",
    "卡方",
    "卡方分布",
    "σ",
    "s",
    "西格马",
    "西格马分布",
    "希格玛",
    "希格玛分布",
    "西格玛",
    "西格玛分布",
)
def rng_chi2():
    domain_min = 0
    domain_max = 18.4668269
    df = 4
    while True:
        val = stats.chi2.rvs(df=df)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("f", "f分布", "f-分布")
def rng_f():
    domain_min = 0
    domain_max = 15.9770248525577
    df1, df2 = 4, 4
    while True:
        val = stats.f.rvs(df1, df2)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("e", "exp", "指数", "指数分布", "geo", "geometric", "几何", "几何分布")
def rng_exp():
    domain_min = 0
    domain_max = 6.9077552789821
    scale = 1
    while True:
        val = stats.expon.rvs(scale=scale)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("c", "cauchy", "柯西", "柯西分布")
def rng_cauchy():
    domain_min = -6.313751514675
    domain_max = 6.313751514675
    loc, scale = 0, 1
    while True:
        val = stats.cauchy.rvs(loc=loc, scale=scale)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("w", "weibull", "威布尔", "威布尔分布", "韦布尔", "韦布尔分布", "韦伯", "韦伯分布", "韦氏分布")
def rng_weibull():
    domain_min = 0
    domain_max = 1.471863002149
    c, scale = 5, 1
    while True:
        val = stats.weibull_min.rvs(c, scale=scale)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("g", "γ", "gamma", "伽马", "伽马分布", "p", "pascal", "帕斯卡", "帕斯卡分布")
def rng_gamma():
    domain_min = 0
    domain_max = 22.45774448485
    alpha, beta = 3, 2
    while True:
        val = stats.gamma.rvs(a=alpha, scale=1 / beta)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("β", "beta", "贝塔", "贝塔分布", "β分布", "b分布", "b-分布")
def rng_beta():
    a, b = 2, 2
    val = stats.beta.rvs(a, b)
    return val  # 本来定义域就是0~1因此不需要拒绝采样


@rngs.named("log", "ln", "logn", "lognorm", "对数正态", "对数正态分布")
def rng_lognorm():
    domain_min = 0
    domain_max = 10.2404736563121
    mu, sigma = 0, 1
    while True:
        val = stats.lognorm.rvs(s=sigma, scale=np.exp(mu))
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named("logistic", "逻辑", "逻辑分布")
def rng_logistic():
    domain_min = -15.586609649449
    domain_max = 15.586609649449
    loc, scale = 5, 2
    while True:
        val = stats.logistic.rvs(loc=loc, scale=scale)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)


@rngs.named(
    "l",
    "lap",
    "laplace",
    "拉普拉斯",
    "拉普拉斯分布",
    "双指数",
    "双指数分布",
)
def rng_laplace():
    domain_min = -4.60517018599
    domain_max = 4.60517018599
    loc, scale = 0, 1
    while True:
        val = stats.laplace.rvs(loc=loc, scale=scale)
        if domain_min <= val < domain_max:
            return (val - domain_min) / (domain_max - domain_min)
