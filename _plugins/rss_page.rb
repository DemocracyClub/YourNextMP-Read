require 'simple-rss'
require 'uri_template'
module Jekyll

  class SingleResultPage < Page
    def initialize(site, base, dir, index, item)
      @site = site
      @base = base
      @dir = dir
      @item = item
      @name = "index.html"
      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'rss_item.html')
      if @item.class == String
        self.data['is_placeholder'] = true
      else
        self.data['item_index'] = index
        self.data['title'] = item.title
        self.data['winner_popit_person_id'] = item.winner_popit_person_id
        self.data['winner_person_name'] = item.winner_person_name
        self.data['winner_party_id'] = item.winner_party_id
        self.data['winner_party_name'] = item.winner_party_name
        self.data['constituency_name'] = item.constituency_name
        self.data['post_id'] = item.post_id

        if item.image_url_template
          tpl = URITemplate.new(item.image_url_template)
          url = tpl.expand('width'=>'0', 'height'=> '80', 'extension'=>'jpg')
          self.data['image_url'] = url
        end



      end
    end
  end

  class ResultsHomePage < Page
    def initialize(site, base, dir, items)
      @site = site
      @base = base
      @dir = dir
      @items = items
      @name = "index.html"
      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'home_page.html')
      self.data['items'] = items
    end
  end

  class ResultPageGenerator < Generator
    safe true

    def generate(site)
      if site.layouts.key? 'rss_page'
        all_pages = []
        dir = 'rss/'
        results_file = '_rss/results.rss'
        require 'rss'
        max_page_id = 0
        open(results_file) do |rss|
          SimpleRSS.item_tags << :"winner_popit_person_id"
          SimpleRSS.item_tags << :"winner_person_name"
          SimpleRSS.item_tags << :"winner_party_id"
          SimpleRSS.item_tags << :"winner_party_name"
          SimpleRSS.item_tags << :"constituency_name"
          SimpleRSS.item_tags << :"image_url_template"
          SimpleRSS.item_tags << :"post_id"
          feed = SimpleRSS.parse(rss)
          items = feed.entries.reverse!
          items.each_with_index do |item, index|
            single_page = SingleResultPage.new(site, site.source, File.join(dir, index.to_s), index, item)
            all_pages << single_page
            site.pages << single_page
            max_page_id += 1
          end
        end
        site.pages << SingleResultPage.new(site, site.source, File.join(dir, max_page_id.to_s), max_page_id, 'placeholder')
        all_pages.reverse!
        site.pages << ResultsHomePage.new(site, site.source, '/', all_pages)

      end
    end
  end

end
