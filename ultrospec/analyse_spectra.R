# open spectrum file
library(tidyverse)
library(readxl)
library(splines)

load_spectra = function(dir){ # dir for xls(x) files
  files = list.files(path = dir, pattern = "*.xls*", ignore.case = T)
  loaded = list()
  for (file in files) {
    label = str_replace(str=file, pat= ".*\\} (.*)\\.[Xx][Ll][Ss][Xx]?", "\\1")
    item_name = ifelse(str_detect(file, fixed("ref", ignore_case = T)), "REF", label)
    loaded[[item_name]] = read_xlsx(paste(dir, file, sep=''), skip = 18)
  }
  return(loaded)
}

smooth.spline2 <- function(formula, data, ...) { 
  mat <- model.frame(formula, data) 
  smooth.spline(mat[, 2], mat[, 1])
} 

predictdf.smooth.spline <- function(model, xseq, se, level) {
  pred <- predict(model, xseq)
  data.frame(x = xseq, y = pred$y)
}

# subtract ref, plot & table the results

analyse_spectra = function(
  loaded_list,
  xlim = c(240, 320),
  ylim = c(0, 0.8),
  smooth.spar = NULL
  ){
  if (!('REF' %in% names(loaded_list))) stop("No reference 'REF' found!")
  sign = ifelse(loaded_list[['REF']]$Absorbance[1]>0, 1, -1)
  result = tibble(Wavelength = loaded_list[['REF']]$Wavelength)
  items = setdiff(names(loaded_list), 'REF')
  for (item in items){
    result[[item]] = (loaded_list[['REF']]$Absorbance - loaded_list[[item]]$Absorbance)*-sign
  }
  res_table = result %>% filter(Wavelength %in% c(260, 280, 320)) %>% t()
  colnames(res_table) = res_table[1,]
  res_table[-1,] %>% round(., 3) %>% print()
  result_l = result %>% gather("Sample", "Signal", -Wavelength)
  print(nrow(result))

  ggplot(result_l, aes(x=Wavelength, y=Signal, col=Sample)) + 
    geom_point(size=2, alpha=.3) + 
    stat_smooth(method='smooth.spline2', se=F) + 
    coord_cartesian(ylim=ylim, xlim=xlim) + 
    #theme(legend.position="bottom", legend.direction='vertical') +
    theme_classic()
}
#analyse_spectra(load_spectra("path"))
