module Jekyll

  class PersonPage < Page
    def initialize(site, base, dir, person)
      @site = site
      @base = base
      @dir = dir

      @name = 'index.html'
      self.process(@name)
      self.read_yaml(File.join(base, '_layouts'), 'person.html')
      self.data['person'] = person
      self.data['hero'] = "#{person['name']}"

    end
  end

  class PersonPageGenerator < Generator
    safe true

    def generate(site)
      if site.layouts.key? 'person'
        dir = 'person/'
        site.data['people']['id'].each_with_index do |person, index|

          # Make the page with just the ID
          site.pages << PersonPage.new(site, site.source, File.join(dir, person[0]), person[1])

          # Make the page with the slug as wel
          slug = Utils.slugify(person[1]['name'])
          site.pages << PersonPage.new(site, site.source, File.join(dir, person[0], slug), person[1])
        end
      end
    end
  end

end
