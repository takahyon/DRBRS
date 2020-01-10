pip install -r requirements.txt
mongo start
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb-community
mkdir -p ~/.nodebrew/src
brew install nodebrew
nodebrew install-binary stable
npm install -g mongoku
