# Достаем группы из отдельной таблицы и динамически добавляем в основную

## Данные

1. Таблица **big**, где есть какие-то данные с наблюдениями, для которых указаны виды (**b**species)

```{r}
# пример большой таблицы
big = data.frame(
  bspecies = c("Rattus rattus", "Rattus rattus", "Rattus norvegicus", "Mus musculus", "Rattus norvegicus", "Canis lupus", "Felis catus"),
  var1 = c(1, 5, 3, 5, 7, 3, 4),
  var2 = c(45, 34, 36, 10, 41, 65, 58)
)
```

```
|bspecies          | var1| var2|
|:-----------------|----:|----:|
|Rattus rattus     |    1|   45|
|Rattus rattus     |    5|   34|
|Rattus norvegicus |    3|   36|
|Mus musculus      |    5|   10|
|Rattus norvegicus |    7|   41|
|Canis lupus       |    3|   65|
|Felis catus       |    4|   58|
``` 

2. Таблица **groups**, где для каждого вида (**g**species) указано, к какой группе он относится

```{r}
# пример таблицы с группами
groups = data.frame(
  gspecies = c("Rattus rattus", "Rattus norvegicus", "Mus musculus", "Canis lupus", "Felis catus"),
  genus = c("Rattus", "Rattus", "Mus", "Canis", "Felis"),
  size = c("small", "small", "small", "big", "big")
)
```

```
|gspecies          |genus  |size  |
|:-----------------|:------|:-----|
|Rattus rattus     |Rattus |small |
|Rattus norvegicus |Rattus |small |
|Mus musculus      |Mus    |small |
|Canis lupus       |Canis  |big   |
|Felis catus       |Felis  |big   |
```
 
## Задача

Создать в таблице **big** дополнительные колонки, в которых будут указаны группы, к которым относится вид, чтобы можно было группировать наблюдения.
 
```{r}
# проверка нормальности (т.к. данных мало - получается фигня)
library(tidyverse)

# считаем для каждой группы shapiro.test
big %>% 
  group_by(bspecies) %>% 
  summarise(normal = shapiro.test(var2)$p.value>0.05)

library(ggpubr)
big %>% ggqqplot("var1", facet.by = "bspecies")

# группировка
library(purrr)
library(magrittr)
big %<>% 
  mutate( # создаем колонки, в которые помещаем соответствующие значения групп из вспомогательной таблицы
    genus = map_chr(bspecies, # для каждого значения из bspecies (таблица big)
                    ~ groups %>% # достаем из таблицы groups ...
                      filter(gspecies == .x) %>% # строку, где gspecies = текущему значению bspecies ...
                      pluck('genus') %>% # из этой строки достаем колонку genus
                      as.character # полученный результат преобразуем в текстовое значение из фактора
                    ),
    size = map_chr(bspecies, 
                   ~ groups %>% 
                     filter(gspecies == .x) %>% 
                     pluck('size') %>% 
                     as.character
                   )
  )

# считаем для каждой НОВОЙ группы среднее и считаем к-во наблюдений в такой группе
big %>% 
  group_by(size) %>% 
  summarise(count = n(), mean = mean(var1))
```
