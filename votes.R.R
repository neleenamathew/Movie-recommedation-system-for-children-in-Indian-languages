# library(rvest)#501 $751  #1001
# library(purrr)
url<-'https://www.imdb.com/search/title/?countries=in&languages=ml&count=250&start=1751&ref_=adv_nxt' 
webpage <- read_html(url)
print(webpage)
id_data_html <- html_nodes(webpage,'.userRatingValue')
id_data <- html_attrs(id_data_html)
id <- id_data %>% map(3)
id<-unlist(id)
# library(stringr)
# library(tidyverse)
# library(tm)
for(i in id)
{
  id_url<-paste0("https://www.imdb.com/title/",i,"/parentalguide?ref_=tt_stry_pg")
  webpage1<-read_html(id_url)
  rank_data_ht1<- html_nodes(webpage1,'.text-primary')
  rank_dat1 <- html_text(rank_data_ht1)
  title_html <- html_nodes(webpage1,".parent")
  title_text[i] <- html_text(title_html)
  title<-gsub("\n","",title_text)
  tite<- str_replace_all(title, "[\r\n\t]", "")
  title<-str_trim(title)
  title_df<-data.frame(Title=title)
  #sexnudity
  sexnudity_html[i] <- html_nodes(webpage1,"#advisory-nudity") %>%
  map_df(~{
    data_frame(
      vote = html_node(.x, "span") %>% html_text(sexnudity_html)
    )
  }) 
 
  sexnudity_df<-data.frame(Sexandnudity=sexnudity_html)

#violence

 violence_html[i]<-html_nodes(webpage1,"#advisory-violence") %>%
 map_df(~{
    data_frame(
      vote = html_node(.x, "span") %>% html_text(trim=TRUE)
    )
  }) 

violence_df<-data.frame(ViolenceGore=violence_html)

#profanity
profanity_html[i]<-html_nodes(webpage1,"#advisory-profanity") %>%
  map_df(~{
    data_frame(
      vote = html_node(.x, "span") %>% html_text(trim=TRUE)
    )
  })
profanity_df<-data.frame(Profanity=profanity_html)


#Alcohol
alcohol_html[i]<- html_nodes(webpage1 ,"#advisory-alcohol")  %>%
  map_df(~{
    data_frame(
      vote = html_node(.x, "span") %>% html_text(trim=TRUE)
    )
  })

alcohol_df<-data.frame(Alcohol=alcohol_html)

#frightening
frightening_html[i]<- html_nodes(webpage1,"#advisory-frightening")  %>%
map_df(~{
  data_frame(
    vote = html_node(.x, "span") %>% html_text(trim=TRUE)
  )
})
frightening_df<-data.frame(Frightening=frightening_html)

}


write.csv(violence_df,"C:\\Users\\USER\\Desktop\\imdb_scraper\\malayalam6vio1.csv")
write.csv(profanity_df,"C:\\Users\\USER\\Desktop\\imdb_scraper\\malayalam6prof.csv")
write.csv(alcohol_df,"C:\\Users\\USER\\Desktop\\imdb_scraper\\malayalam6alc.csv")
write.csv(frightening_df,"C:\\Users\\USER\\Desktop\\imdb_scraper\\malayalam6fright.csv")
write.csv(title_df,"C:\\Users\\USER\\Desktop\\imdb_scraper\\malayalam6titles.csv")
write.csv(sexnudity_df,"C:\\Users\\USER\\Desktop\\imdb_scraper\\malayala6sexandnudity.csv")  
