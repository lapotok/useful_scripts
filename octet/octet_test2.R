library(tidyverse)
library(magrittr)
library(ggplot2)

# fn = file.choose()
fn = "/Volumes/Document/Octet/Octet results/2019-02-14 SA+SAX loading test (TnAB+B)/Results/2019_02_19 13_26_50 Preprocessed Data-Assay1.csv"

# read the file
con = file(fn, "r")
count = 0
while (TRUE) {
  line = readLines(con, n = 1)
  if (!(substring(line, 1, 1) %in% c(" ", "\t", "<"))) break
  count = count + 1
}
close(con)

reads = rio::import(fn, skip = count)
reads = reads %>% dplyr::select_if(~sum(!is.na(.)) > 0) # skip na cols
reads = reads %>% set_colnames(paste(reads[2,], reads[1,]))
reads = reads[ -(1:4),]

reset_time = function(x){x-x[1]}
reads = reads %>% mutate_all(as.numeric) %>% mutate_at(vars(starts_with("Sample Loc")), funs(reset_time))

reads = 
  reads %>% 
  mutate(n = row_number()) %>% 
  gather(var, val, -n) %>% 
  separate(var, c("type", "sensor"), sep = ": ") %>% 
  spread("type", "val") %>%
  arrange(sensor, `Sample Loc`) 


reads_1 = 
  reads %>% 
  filter(sensor == "t1C4c1") %>% 
  select(-n, -sensor) %>% 
  set_colnames(c("y", "x"))

