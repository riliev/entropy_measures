Background:
In an 2011 PNAS paper the authors claimed that the length of the word is predicted by its information content, where information content is measures as conditional entropy (given the preceding word). The idea is that words with higher information are longer because language follows the principlie of “uniform information density”, where  a relatively constant amount of information is transferred per unit time. 

Purpose:
I was curious if the forward measure of entropy (conditioned on the preceding word) is a similarly good predictor as backward entropy (conditioned on the subsequent word). For large random variables it is easy to show that these two are the same, but it is not clear if they are similar in relatively small text corpora (e.g. a few million words).

Files:
concat_files.py assembles a text corpus from various txt files
compute_entropy.py computes forward and backward entropies for each word
compare_entropies.R is R code which runs some basic statistical analyses on the resulting

Conclusion:
It seemse that even in small text corpora forward and backward entropy is pretty much the same (Pearson r = .99). 


