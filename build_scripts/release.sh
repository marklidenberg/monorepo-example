#!/usr/bin/env bash

cd ..

# - получаем версию
pyproject_contents=$(cat pyproject.toml)

# парсим версию
regex_pattern='version = "([0-9\.]+)"'
# применяем regex, результат сохранится в BASE_REMATCH
[[ $pyproject_contents =~ $regex_pattern ]]
VERSION=${BASH_REMATCH[1]} # 0.2.22

# - генерим ченджлог
auto-changelog --latest-version "$VERSION" --tag-pattern "release"

# - пушим изменения с новым релизом
git checkout master
git commit -a -m "chore(release): $VERSION"
git tag -a "release-$VERSION" -m "chore(release): $VERSION" HEAD
git push
git push origin "release-$VERSION"

cd build_scripts
