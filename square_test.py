import market_environment as me
import datetime as dt
import constant_short_rate as constant
import geometric_brownian_motion as geometric
import matplotlib.pyplot as plt
import simulation_class as sim
import jump_diffusion as jump
import square_root_diffusion as square
me_gbm = me.market_environment('me_gbm' , dt.datetime(2015, 1, 1))
me_gbm.add_constant('initial_value' , 36.)
me_gbm.add_constant('volatility' , 0.2)
me_gbm.add_constant('final_date' , dt.datetime(2015, 12, 31))
me_gbm.add_constant('currency' , 'EUR')
me_gbm.add_constant('frequency' , 'M')
# monthly frequency (respective month end)
me_gbm.add_constant('paths' , 10000)
csr = constant.constant_short_rate('csr',0.05)
me_gbm.add_curve('discount_curve',csr)
gbm = geometric.geometric_brownian_motion('gbm',me_gbm)
gbm.generate_time_grid()
#print(gbm.time_grid)
paths_1 = gbm.get_instrument_values()
#print(paths_1)
gbm.update(volatility=0.5)
paths_2 = gbm.get_instrument_values()
plt.figure(figsize= (8,4))
p1 = plt.plot(gbm.time_grid,paths_1[:,:10],'b')
p2 = plt.plot(gbm.time_grid,paths_2[:,:10],'r-.')
plt.grid(True)
l1 = plt.legend([p1[0],p2[0]],['low volatility','high volatility'],loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.show()

me_jd = me.market_environment('me_jd',dt.datetime(2015,1,1))
me_jd.add_constant('lambda',0.3)
me_jd.add_constant('mu',-0.75)
me_jd.add_constant('delta',0.1)
me_jd.add_environment(me_gbm)

jd = jump.jump_diffusion('jd',me_jd)
paths_3 = jd.get_instrument_values()
jd.update(lamb=0.9)#改变跳动频率
paths_4 = jd.get_instrument_values()
plt.figure(figsize= (8,4))
p1 = plt.plot(gbm.time_grid,paths_3[:,:10],'b')
p2 = plt.plot(gbm.time_grid,paths_4[:,:10],'r-.')
plt.grid(True)
l1 = plt.legend([p1[0],p2[0]],['low intensity','high intensity'],loc=3)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.show()

me_srd = me.market_environment('me_srd' , dt.datetime(2015, 1, 1))
me_srd.add_constant('initial_value' , .25)
me_srd.add_constant('volatility' , 0.05)
me_srd.add_constant('final_date' , dt.datetime(2015, 12, 31))
me_srd.add_constant('currency' , 'EUR')
me_srd.add_constant('frequency' , 'W')
# monthly frequency (respective month end)
me_srd.add_constant('paths' , 10000)
me_srd.add_constant('kappa' , 4.0)
me_srd.add_constant('theta' , 0.2)
me_srd.add_curve('discount_curve',constant.constant_short_rate('r',0.0))

srd = square.square_root_diffusion('srd',me_srd)
srd_paths = srd.get_instrument_values()[:,:10]

plt.figure(figsize= (8,4))
plt.plot(srd.time_grid,srd.get_instrument_values()[:,:10])
plt.axhline(me_srd.get_constant('theta'),color='r',ls='-',lw=2.0)
plt.grid(True)
plt.xticks(rotation=30)
plt.show()