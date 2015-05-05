module Jekyll
  module NumberFilters
    def round(number)
      '%.1f' % number
    end
  end

  module PopitFilters
    def fixproxyurl(value)
        if not value
            return ''
        end

        # Some PopIt versions have a double-slash accidentally included:
        result = value.sub('image-proxy//', 'image-proxy/')

        # Force HTTPS in images
        result = result.sub('^http://', 'https://')

        return result
    end
  end
end

Liquid::Template.register_filter(Jekyll::NumberFilters)
Liquid::Template.register_filter(Jekyll::PopitFilters)
