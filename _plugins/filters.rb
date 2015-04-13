module Jekyll
  module NumberFilters
    def round(number)
      '%.1f' % number
    end
  end
end

Liquid::Template.register_filter(Jekyll::NumberFilters)