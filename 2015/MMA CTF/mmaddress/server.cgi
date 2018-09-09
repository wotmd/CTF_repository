#!/usr/bin/ruby
require 'cgi'
require 'securerandom'
require 'mongo'
require 'erb'
require 'json'


connection = Mongo::Connection.new
db = connection.db('sp')

cgi = CGI.new
path = cgi.path_info[1..-1]
base_path = File.expand_path(File.join(__FILE__, '..'))
view_path = File.expand_path(File.join(base_path, 'views'))
controller_path = File.expand_path(File.join(base_path, 'controllers'))
CONFIG = JSON.parse(File.read(File.join(base_path, 'config.json')))
FLAG = CONFIG['FLAG2']

# Load Session
require File.join(controller_path, 'session')
session = cgi.cookies['session'][0] || ''
session = Session.new(session)

def redirect_to(cgi, path, session = nil)
  cgi.out ( { 'cookie' => session ? [session.to_cookie] : [], 'status' => 'REDIRECT', 'location' => path} ) { '' }
  exit
end

# routing
case path
when /^login$/
  if cgi.request_method == 'POST'
    user, password = cgi.params['user'][0].to_s, cgi.params['password'][0].to_s
    user = user.downcase
    user = db.collection('user').find(user: user, password: MyHash.new.hex_hash(password)).to_a[0]
    if user
      session.set("user", user['user'])
      session.set("password", user['password'])
      redirect_to cgi, '/', session
    else
      error = true
    end
  else
    error = false
  end
  view = ERB.new(File.read(File.join(view_path, 'login.html.erb'))).result

when /^logout$/
  session.set("user", nil)
  redirect_to cgi, '/', session

when /^register$/
  error = false
  if cgi.request_method == 'POST'
    user, password = cgi.params['user'][0].to_s, cgi.params['password'][0].to_s
    begin
      user = user.downcase
      raise StandardError.new if user.size >= 12
      db.collection('user').insert(user: user, password: MyHash.new.hex_hash(password), frozen: false)
      redirect_to cgi, '/'
    rescue => e
      STDERR.puts e
      error = true
    end
  end
  view = ERB.new(File.read(File.join(view_path, 'register.html.erb'))).result

when /^new$/
  redirect_to cgi, '/' unless session.get('user')
  user = db.collection('user').find(user: session.get('user').to_s).to_a[0]
  redirect_to cgi, '/' if user['frozen']
  url = cgi.params['url'][0].to_s.split.join
  redirect_to cgi, '/' unless /^https?:\/\// =~ url || url.size > 100
  db.collection('shorten').insert(
    user: user['user'].to_s,
    param: SecureRandom.hex(12),
    url: url
  )
  redirect_to cgi, '/'

when /^jump\/([0-9a-f]+)/
  param = $1

  shorten = db.collection('shorten').find(param: param).to_a[0]
  redirect_to cgi, shorten['url']
else
  if session.get('user')
    user = db.collection('user').find(user: session.get('user').to_s).to_a[0]
    urls = db.collection('shorten').find({user: user['user']}, limit: 10, sort: {_id: -1}) if user
  end
  view = ERB.new(File.read(File.join(view_path, 'index.html.erb'))).result
end

cgi.out do
  ERB.new(File.read(File.join(view_path, 'layout.html.erb'))).result
end
