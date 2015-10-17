#!/usr/bin/env ruby


require 'optparse'
require 'nokogiri'

#declare commandline options
options = {}
parser = OptionParser.new do |opts|
  opts.banner = 'Usage bomizer.rb -p path-to-directory'

  opts.on('-p path', '--path path', 'path to directory containing pom.xml to strip versions') do |path|
    if Dir.exists? path
      options[:path] = path
    else
      puts "path: #{path} is not valid directory"
      exit 1
    end
  end

  opts.on('-m mask', '--mask', 'process only files with this name. Defaults to pom.xml') do |mask|
    options[:mask] = mask
  end
end

parser.parse!

if not options[:path]
  puts "Missing path argument"
  exit 1
end


class Bomizer

  attr_accessor :mask, :path

  def initialize (path, mask = 'pom.xml')
    @path = path
    @mask = mask
  end

  # find all files matching @mask in @path
  def find_files
    @files = Dir.glob("#{@path}/**/#{@mask}")
    puts "found #{@files.length} matching '#{@mask}' in directory #{@path}"
    return @files
  end


  # it takes path to xml file and removes elements project/dependencies/dependency/version
  # :file_path: path to xml file
  def strip_versions file_path

    xml_content = ''
    File.open(file_path, 'r') do |source|
      # create xml dom
      doc = Nokogiri::XML source
      # find project/dependencies node, skip if nothing found
      dependencies = doc.root.children.at('dependencies')
      return unless dependencies # skip if there are no dependencies in xml

      # traverse dependencies/dependency and remove version element from dependency
      dependencies.search('dependency').each do |dep|
        dep.element_children.at('version').remove if dep.element_children.at('version')
      end
      # store modified xml to var
      xml_content = doc.to_xml
    end
    # replace original xml with modified
    File.open(file_path, 'w') do |dest|
      dest.puts xml_content
    end
  end

  # remove dependency versinon recursively from all files matching mask in @path
  def strip_recursively
    find_files.each do |file|
      strip_versions file
    end
    puts "successfuly checked #{@files.length} files and removed dependency version if some was defined"
  end
end


bom = Bomizer.new options[:path]
bom.mask = options[:mask] if options[:mask]
bom.strip_recursively