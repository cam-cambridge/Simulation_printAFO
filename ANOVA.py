import pandas as pd
import statsmodels.api as sm
from statsmodels.formula.api import ols
import scipy.stats

A=[12.6, 12, 11.8, 11.9, 13, 12.5, 14]
B=[10, 10.2, 10, 12, 14, 13]
C=[10.1, 13, 13.4, 12.9, 8.9, 10.7, 13.6, 12]
all_scores=A+B+C
company_names=(['A']*len(A))+(['B']*len(B))+(['C']*len(C))
data=pd.DataFrame({'company': company_names, 'score': all_scores})
data.groupby('company').mean()

# ANOVA using statsmodels
lm=ols('score ~ company', data=data).fit()
table=sm.stats.anova_lm(lm)

# ANOVA using maths and python scratch
# Compute overall mean
overall_mean=data['score'].mean()

 # Compute sum of squares total
data['overall_mean']=overall_mean
ss_total=sum((data['score']-data['overall_mean'])**2)
ss_total
# Compute group means
group_means = data.groupby('company').mean()
group_means=group_means.rename(columns={'score': 'group_mean'})
# Add group means and overall mean to the original data DataFrame
data=data.merge(group_means, left_on='company', right_index=True)
# Compute sum of squares residual
ss_residual = sum((data['score']-data['group_mean'])**2)
# Compute sum of squares model
ss_explained=sum((data['overall_mean_x']-data['group_mean'])**2)
# Compute mean square ss_residual
n_groups=len(set(data['company']))
n_obs=data.shape[0]
df_residual=n_obs-n_groups
ms_residual=ss_residual / df_residual
# Compute mean squre explained
df_explained=n_groups-1
ms_explained=ss_explained / df_explained

# Compute F-value
f=ms_explained / ms_residual
# Compute p-value
p_value=1-scipy.stats.f.cdf(f, df_explained, df_residual)
print(p_value)
