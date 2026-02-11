In order to run the website locally, you have to:

1. Install required packages:
```
sudo apt-get install ruby-full build-essential zlib1g-dev
```

2. (optional) Modify Gems to be installed in home directory:
```
echo '# Install Ruby Gems to ~/gems' >> ~/.bashrc
echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc
echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

3. Install `jekyll` and `bundler` gems:
```
gem install jekyll bundler
```

4. Create Gemfile in the `icra2026_race` folder with following lines:
```
source "https://rubygems.org"
gem "github-pages", group: :jekyll_plugins
```

5. Install the website:
```
bundle install
```

6. Run the website locally:
```
bundle exec jekyll serve
```

7. Open the browser at:
```
http://localhost:4000
```

The webpage refreshes when any file is changed. For some more drastic changes, you have to repeat step 6.