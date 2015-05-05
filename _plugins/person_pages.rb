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

      if person['candidacies'].key? 'ge2015'
        title = "#{person['name']}, #{person['candidacies']['ge2015']['party']['name']} candidate to be MP for #{person['candidacies']['ge2015']['constituency']['name']}"
      else
        title = "#{person['name']}"
      end
      self.data['title'] = title

      if person['candidacies'].key? 'ge2015'
        last_party = person['candidacies']['ge2015']['party']
        last_constituency = person['candidacies']['ge2015']['constituency']
        last_year = 2015
      elsif person['candidacies'].key? 'ge2010'
        last_party = person['candidacies']['ge2010']['party']
        last_constituency = person['candidacies']['ge2010']['constituency']
        last_year = 2010
      else
        last_party = last_constituency = last_year = nil
      end

      if last_year == 2015
        description = "#{person['name']} is standing "
      elsif last_year == 2010
        description = "#{person['name']} stood "
      else
        description = "#{person['name']}"
      end
    
      if last_year == 2015 || last_year == 2010
        party_name = last_party['name']
        constituency_name = last_constituency['name']

        if party_name == "Independent"
          description += "as an independent candidate"
        else
          if party_name.split(' ')[0] == 'The'
            description += 'for'
          else
            description += 'for the'
          end
          description += " #{party_name}"
        end

        description += " in #{constituency_name} in #{last_year} - find out more on YourNextMP"
      end
      self.data['description'] = description

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
