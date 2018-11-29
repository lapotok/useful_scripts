# read XLSX file into a matrix with 1:12 x A:H dimensions
read_plate = function(fn){
  # import Multiscan files *.001 etc. 
  # TODO
    
  # import XLS(x) files 
  require(tidyverse)
  require(readxl)
  plate = fn %>%
    read_xls(sheet=2, skip = 5, n_max = 8) %>%
    as.matrix()
  dimnames(plate) = list(LETTERS[1:8], 1:12)
  return(plate)
}

parse_plate = function(x){
  # set range: A1:H12, v(ertical)/h(orizontal), start_conc=100, rate=1/3
  # 

}

read_xl_copypasted = function(text){}

build_calibr_curve = function(x){}

calc_conc_with_calibr = function(x){}
