mkdir -p _rss
curl "https://yournextmp.com/results/all.atom" -fsS |  xmlindent > _rss/results.rss
