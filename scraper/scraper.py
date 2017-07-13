def make_urls():
    baseurl = "http://www.seinology.com/scripts/script-"
    special_eps = [82, 83, 100, 101, 177, 178, 179, 180]
    urls = []
    for episode in range(1, 180):
        if episode not in special_eps:
            url = "{baseurl}{num}.shtml".format(baseurl=baseurl, num=str(episode).zfill(2))
            urls.append(url)
    special_urls = ['82and83', '100and101', '177and178', '179and180']
    for special_url in special_urls:
            url = "{baseurl}{num}.shtml".format(baseurl=baseurl, num=special_url)
            urls.append(url)
    return urls

