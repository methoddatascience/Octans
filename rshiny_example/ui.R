# ui_fluidpage takes care of browser width


shinyUI(pageWithSidebar(
  headerPanel("Social Media Expertise of Business Schools"),
  
  # Inputs
  
  sidebarPanel(
    # selectInput(inputId = "type",
    #                        label = "Searching for User or Keyword?",
    #                        choices = c("User", "Keyword"),
    #                        selected="User"),
               textInput(inputId = 'keyword1', label = "Enter a soft skill keywword", placeholder = ""),
               textInput(inputId = 'keyword2', label = "Enter teaching related keywword", placeholder= ""),
               textInput(inputId = 'keyword3', label = "Enter domain relavant keywword", placeholder= ""),
               # selectInput("tweettype", label = "What tweets do you want to focus on:",
               #             c("All Tweets" = c("fav", "noeng", "ret",
               #               "Those that got Favorited" = "fav",
               #               "Those that got Retweeted" = "ret",
               #               "Those that got Favorited or Retweeted" = "favret")),
               #sliderInput("cant", "Select number of Tweets",min=5,max=1500, value = 5),
               submitButton(text = "Run")
               # would be good to have a done button/message
               
               #downloadButton("download", "Download File"),
               #downloadButton("download", "Download the Report")
               ),
  
  mainPanel( # what to put in the main panel. maybe first draw it out
    # need to find a way to not show any results before selecting run
    h3("The data set contains the first 1000 tweets from UMSBE, CBSSchool, and LUISS Business School.
       This is an example of a dashboard."),
    verbatimTextOutput("summary"),
    h4("Tweets"),
    #dataTableOutput("table"),
    p("Tweets aggregated per day for the 3 business schools"),
    plotOutput(outputId = "plot1"),
    p("Tweets aggregated per Keyword and day for the 3 business schools"),
    plotOutput(outputId = "plot2")
   # verbatimTextOutput("value")
    )
))

library(shiny)
library(twitteR)
library(wordcloud)
library(tm)
library(dplyr)
library(ggplot2)
library(stringi)

consumerKey = "My Key"
consumerSecret = "My Secret"
accessToken = "My Token"
accessSecret = "My Secret"
my_oauth <- setup_twitter_oauth(consumer_key='0i2JCz10FhsWrJmgy7iLldVXp',
                                consumer_secret='nkIgmAQ6at24ydUnm5olrOY64OqJ1fHFwYOVYQ636HvJ1mewSy',
                                access_token='2220997760-6XDKYaSCv3D0jPJ9XRRG5dhOSzmjwc88llGbUa2',
                                access_secret='ZIMBaNce0ltCeOooPn9giK3lKPNgmUs78rHHoua09ZoQ8')


