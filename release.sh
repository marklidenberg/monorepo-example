#!/usr/bin/env bash
# - сборка нового релиза
if [ -z $* ]
  then
  echo "No options found!"
  exit 1
fi

if [ "$1" != "major" ] && [ "$1" != "minor" ] && [ "$1" != "patch" ];
  then
  echo "you must specify: major, minor or patch"
  exit 1
fi

# - меняем релиз в чарте
poetry_output=$(poetry version $1) # 'Bumping version from 0.2.22 to 0.2.23'

# парсим версию
regex_pattern='from ([0-9\.]+) to ([0-9\.]+)'
# применяем regex, результат сохранится в BASE_REMATCH
[[ "$poetry_output" =~ $regex_pattern ]]
VERSION_FROM=${BASH_REMATCH[1]} # 0.2.22
VERSION=VERSION_TO=${BASH_REMATCH[2]} # 0.2.23

echo "Bumping $1 version from $VERSION_FROM to $VERSION_TO"

# - генерим ченджлог
auto-changelog --latest-version "$VERSION" --tag-pattern "release"

# - пушим изменения с новым релизом
git checkout master
git commit -a -m "chore(release): $VERSION"
git tag -a "release-$VERSION" -m "chore(release): $VERSION" HEAD
git push
git push origin "release-$VERSION"