require 'json'
require_relative 'myhash'
require_relative 'hmac'

class Session
  def initialize(cookie)
    @session = {}
    @hash = MyHash.new
    begin
      json, hmac = cookie.split('-----').map do |b64|
        b64.unpack("m")[0]
      end
      if HMAC.hmac(json, FLAG, 512) { |msg| @hash.str_hash(msg) } == hmac
        @session = JSON.parse(json)
      end
    rescue StandardError => e
    end
  end

  def get(key)
    @session[key]
  end

  def set(key, value)
    @session[key] = value
  end

  def to_cookie
    str = ([@session.to_json].pack('m') + '-----' + [HMAC.hmac(@session.to_json, FLAG, 512) { |msg| @hash.str_hash(msg) }].pack('m')).split.join
    CGI::Cookie.new(
      'name' => 'session',
      'value' => str
    )
  end
end
