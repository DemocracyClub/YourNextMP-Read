module Jekyll

  class ConstituencyPage < Page
    def initialize(site, base, dir, constituency)
      @site = site
      @base = base
      @dir = dir

      @name = 'index.html'
      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'constituency.html')
      self.data['constituency'] = constituency
      self.data['title'] = "Candidates to be MP (PPCs) for #{constituency['mapit']['name']} in the UK 2015 General Election"
      self.data['hero'] = "Candidates to be MP for #{constituency['mapit']['name']}"
      self.data['description'] = "List of candidates to be MP (PPCs) for #{constituency['mapit']['name']} in the UK 2015 General Election - find out more on YourNextMP"

    end
  end

  class ConstituencySlugPage < Page

    def initialize(site, base, dir, constituency)
      @site = site
      @base = base
      @dir = dir

      @name = 'index.html'
      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'constituency.html')
      self.data['constituency'] = constituency
      self.data['title'] = "Candidates to be MP (PPCs) for #{constituency['mapit']['name']} in the UK 2015 General Election"
      self.data['hero'] = "Candidates to be MP for #{constituency['mapit']['name']}"
      self.data['description'] = "List of candidates to be MP (PPCs) for #{constituency['mapit']['name']} in the UK 2015 General Election - find out more on YourNextMP"

    end
  end


  class ConstituencyPageGenerator < Generator
    safe true

    def generate(site)
      if site.layouts.key? 'constituency'
        dir = 'constituency/'
        site.data['constituencies']['id'].each_with_index do |constituency, index|

          # Make the page with just the ID
          site.pages << ConstituencyPage.new(site, site.source, File.join(dir, constituency[0]), constituency[1])

          # Make the page with the slug as wel
          slug = Utils.slugify(constituency[1]['mapit']['name'])
          site.pages << ConstituencyPage.new(site, site.source, File.join(dir, constituency[0], slug), constituency[1])
        end
      end
    end
  end

end
