# -*- encoding: utf-8 -*-
require File.expand_path("../lib/rubyfunge/version", __FILE__)

Gem::Specification.new do |s|
  s.name        = "rubyfunge"
  s.version     = Rubyfunge::VERSION
  s.platform    = Gem::Platform::RUBY
  s.authors     = ['Zoltan Dezso']
  s.email       = ['dezso.zoltan@gmail.com']
  s.homepage    = "http://github.com/zaki/rubyfunge"
  s.summary     = "A Befunge-93 interpreter written in ruby."
  s.description = "A Befunge-93 interpreter written in ruby."

  s.required_rubygems_version = ">= 1.3.6"
  s.rubyforge_project         = "rubyfunge"

  s.add_development_dependency "bundler", ">= 1.0.0"

  s.files        = `git ls-files`.split("\n")
  s.executables  = `git ls-files`.split("\n").map{|f| f =~ /^bin\/(.*)/ ? $1 : nil}.compact
  s.require_path = 'lib'
end
