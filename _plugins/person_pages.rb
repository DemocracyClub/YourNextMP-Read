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
        site.data['people'].each_with_index do |person, index|
          if ENV['BUILD_LIMIT'].to_i <= index
            puts person
            puts index
            site.pages << PersonPage.new(site, site.source, File.join(dir, person[0]), person[1])
          end
        end
      end
    end
  end

end
