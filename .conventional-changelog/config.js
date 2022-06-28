const Handlebars = require('handlebars');
const fs = require('fs');
const path = require('path');

/**
 * Только эти типы коммитов попадают в ченджлог
 */
const types = {
  feat: 'Features',
  fix: 'Bug Fixes',
  refactor: 'Refactoring',
  revert: 'Reverts',
};

module.exports = {
  options: {
    // debug: console.debug.bind(console),

    tagPrefix: 'release-',
  },

  parserOpts: {
    /**
     * Настройки автоматической вставки ссылок на issue tracker
     */

    // issuePrefixes: ['PROJ-'],
    // issuePrefixesCaseSensitive: true,
    // issueUrlFormat: 'https://deeplay.atlassian.net/browse/PROJ-{{id}}',

    referenceActions: null,
    /**
     * Секции примечаний из всех коммитов будут объединены в один список в
     * релизе
     */
    noteKeywords: ['## Примечания'],
    notesPattern: noteKeywordsSelection =>
      new RegExp('^[\\s|*]*(' + noteKeywordsSelection + ')[:\\s]*(.*)', 'i'),
  },

  writerOpts: {
    transform(commit, root) {
      const getPullRequestLink = issue =>
        `[#${issue}](${root.repoUrl}/pull/${issue})`;

      if (commit.subject) {
        commit.subject = commit.subject.replace(/#(\d+)/g, (_, issue) =>
          getPullRequestLink(issue),
        );
      }

      commit.header = commit.header.replace(/#(\d+)/g, (_, issue) =>
        getPullRequestLink(issue),
      );

      if (commit.body) {
        commit.indentedBody = commit.body
          .split('\n')
          .map(line => `  ${line}`)
          .join('\n');
      }

      for (const note of commit.notes) {
        note.title = note.title.replace(/^## /, '');
        note.text = note.text
          .split('\n')
          .map((line, i) => (i === 0 ? line : `  ${line}`))
          .join('\n');
      }

      return commit;
    },

    mainTemplate: fs.readFileSync(path.join(__dirname, 'template.hbs'), 'utf8'),
    commitPartial: fs.readFileSync(path.join(__dirname, 'commit.hbs'), 'utf8'),
    footerPartial: fs.readFileSync(path.join(__dirname, 'footer.hbs'), 'utf8'),
  },
};

Handlebars.registerHelper('shortHash', hash => hash.slice(0, 7));
Handlebars.registerHelper(
  'filterCommitGroups',
  group => types[group.title] != null,
);
Handlebars.registerHelper('getCommitGroupTitle', group => types[group.title]);
