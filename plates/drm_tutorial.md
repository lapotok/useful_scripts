# Тестовые данные

```r
rd = structure(list(Sample = c("-70", "-70", "-70", "-70", "-70",  "-70", "-70", "-70", "+04", "+04", "+04", "+25", "+25", "+25",  "+37", "+37", "+37", "+45", "+45", "+45"), Conc = c(204, 85.4,  35.75, 14.96, 6.26, 2.62, 0, 0, 85.4, 35.75, 14.96, 85.4, 35.75,  14.96, 85.4, 35.75, 14.96, 85.4, 35.75, 14.96), X1 = c(282361,  170122, 66986, 18739, 5509, 2375, 1599, 988, 171092, 62772, 19661,  149759, 53459, 14310, 129832, 44176, 15786, 100717, 38131, 11528 ), X2 = c(290075, 162790, 61082, 17862, 5685, 2179, 1137, 1021,  154515, 57584, 19520, 130656, 54740, 16164, 134473, 57389, 15510,  146733, 40097, 11768), X3 = c(300561, 168721, 64956, 18628, 5387,  2146, 992, 1323, 181300, 58114, 17612, 146885, 49525, 15906,  157206, 53788, 14981, 108051, 34220, 11340)), class = "data.frame", row.names = c(NA,  -20L))
ref.name = "-70"
```

# Пример анализа

```r
# ============= грузим библиотеки ============= #
library(drc)
library(tidyverse)

# ============= фитируем калибровку ============= #
ld = rd %>% gather("Run", "Value", -Sample, -Conc)   # реформатирование
calibr = ld %>% filter(Sample == ref_name)           # берем только калибровку
calibr_m = drm(Value~Conc, data=calibr, fct=LL.5())  # генерация модели
calibr_mb = boxcox(calibr_m, plotit=F)               # уточнение модели
confint(calibr_mb)                                   # доверительные интервалы коэффициентов (b=slope)
# modelFit(calibr_mb)
# compParm(calibr_mb, "b", "-")

# ============= строим график ============= #
# строим кривую по точкам от "нуля"
pred_xlim = c(
  ifelse(min(calibr$Conc) == 0, min(calibr$Conc[calibr$Conc > 0])/10, min(calibr$Conc)),
  max(calibr$Conc)
)
pred = expand.grid(conc=exp(seq(log(pred_xlim[1]), log(max(calibr$Conc)), length=100)))
pm = predict(calibr_mb, newdata=pred, interval="confidence")
pred$p <- pm[,1]
pred$pmin <- pm[,2]
pred$pmax <- pm[,3]
# adjust 0
calibr$Conc0 <- calibr$Conc
calibr$Conc0[calibr$Conc0 == 0] <- pred_xlim[1]

ggplot(calibr, aes(x = Conc0, y = Value)) +
  geom_point(size=5, alpha=.4, na.rm = T) +
  geom_ribbon(data=pred, aes(x=conc, y=p, ymin=pmin, ymax=pmax), alpha=0.2) +
  geom_line(data=pred, aes(x=conc, y=p)) +
  scale_x_log10() +
  scale_y_log10() + 
  annotation_logticks(sides="lb") +
  coord_cartesian(xlim = c(pred_xlim[1]*0.9,pred_xlim[2]*1.2), ylim=c(min(pred$pmin)*0.5, max(pred$pmax))*1.5, expand = F) +
  xlab("Концентрация белка, нг/мл") + ylab("Сигнал (CPS)") +
  theme_classic() 
```

Формула функции 5PL

<a href="https://www.codecogs.com/eqnedit.php?latex=f(x,(b,c,d,e,f))=c&plus;\frac{d-c}{(1&plus;exp(b\cdot(\log(x)-\log(e))))^f}" target="_blank"><img src="https://latex.codecogs.com/gif.latex?f(x,(b,c,d,e,f))=c&plus;\frac{d-c}{(1&plus;exp(b\cdot(\log(x)-\log(e))))^f}" title="f(x,(b,c,d,e,f))=c+\frac{d-c}{(1+exp(b\cdot(\log(x)-\log(e))))^f}" /></a>

Смысл коэффициентов

* **B** - наклон кривой
* **C** - сигнал в точке с нулевой концентрацией
* **D** - сигнал в точке с бесконечно большой концентрацией
* **E** - точка перегиба кривой (центральная точка)
* **F** - фактор ассимметрии

Дальнейшие шаги

* Mixed effects
* Outlier detection
  - https://www.graphpad.com/guides/prism/6/statistics/index.htm?stat_checklist_identifying_outliers.htm
  - https://www.graphpad.com/support/faqid/1598/
  - https://www.unistat.com/bioassay-analysis/
  - https://www.unistat.com/guide/bioassay-analysis-overview/#u1002
  - https://www.unistat.com/guide/bioassay-analysis-overview/#u1006
  - https://www.unistat.com/guide/goodness-of-fit-outlier-tests/
  - https://www.unistat.com/guide/bioassay-analysis-parallel-line-method/#u10121
* Итерации ремоделлирования при удалении outliers из калибровки
* Отчет в Excel
