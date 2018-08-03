# Octans

# Week 4 Notes
#
# Client Information
- parkinson disease treated with light therapy and not pharmaceutical treatment.
- Looking for: broader tool that can help in other medical device startups to identify market trends and areas that are ready for (technological ?) innovations
- Not much radical innovation in treatment of parkinson disease
## Data science aspect:
What diseases have not seen a breakthrough in treatment. Meaning that a disease is treated without much success (?) for several years (+10?), but no breakthrough in treatment has been reported. A disease is treated without success if it only delays dying, i.e., the symptoms are reduced but not removed.
- Involves Natural Language Processing (NLP), data visualization, predictive machine learning


## Questions (point 3 in 'method' method)
* What is the best approach?
  * 'scraper.py' gets papers from pubmed
  * search terms can be identified with the 'neurological_disorders.md' document
  * Get papers from the last 20 years and measure progress:
    * top 100 papers of each year?
      * Can we find citation frequencies?
    * fraction of all papers in top journals each year?
      * scimago lists journal rankings
  * 'scrape_cordis.ipynb' finds funded projects
  * How do we use funding data?
    * Use search terms as above and identify trends in funding over last 20 years

## Predicting Innovation
* Uzzi: atypical combinations of citations
  * create full citation network based on collected data
  * pairwise combinations of referneces in bibliograph of each paper. So link between focal paper and paper in reference list. this is done for all papers in the reference list. 
  * frequency of journal pairing is counted
  * frequency of each co-citation pairs. Compare this frequency with expected change using randomized citation networks
    * switching algorithm: monte carlo simulations (MCMC)
  * aggregate counts of paper pairs into journals
