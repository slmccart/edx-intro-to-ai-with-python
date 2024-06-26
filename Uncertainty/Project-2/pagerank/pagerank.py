import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    model = {}

    # If current page has no outgoing links, probability is equally divided across all pages
    if len(corpus[page]) == 0:
        for cpage in corpus:
            model[cpage] = 1 / len(corpus)
    else:
        # Populate model with pages and initial probability of selecting page at random
        for cpage in corpus:
            model[cpage] = (1 - damping_factor) / len(corpus)

        # Increase probability of pages linked from current page equally
        for link in corpus[page]:
            model[link] += damping_factor / len(corpus[page])

    return model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Seed dictionary with all pages and an initial value of 0
    ranks = {}
    for page in corpus:
        ranks[page] = 0

    # Generate first sample randomly
    current_page = random.choice(list(ranks))
    ranks[current_page] += 1 / n

    # For subsequent samples between 1 (inclusive) and n (exclusive), use transition model
    #  to select a weighted choice for the next sample
    if n > 1:
        for i in range(1, n):
            model = transition_model(corpus, current_page, damping_factor)
            current_page = random.choices(
                population=list(model.keys()),
                weights=model.values(),
            )

            # random.choices returns a list of choices, so pop the first since we only care about
            #  one choice at a time
            current_page = current_page.pop()
            ranks[current_page] += 1 / n

    return ranks


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
