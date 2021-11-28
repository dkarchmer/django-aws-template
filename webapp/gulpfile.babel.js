// generated on 2016-03-23 using generator-webapp 2.0.0
import gulp from 'gulp';
import browserSync from 'browser-sync';
import del from 'del';
import {stream as wiredep} from 'wiredep';
import replace from 'gulp-replace';
var gulpLoadPlugins = require('gulp-load-plugins');

const $ = gulpLoadPlugins();
const reload = browserSync.reload;

const config = {
  htmlFiles: 'src/*.html',
  imageFiles: 'src/app/images/**/*',
  fontFiles: 'src/app/fonts/**/*',
  scssFiles: 'src/app/styles/*.scss',
  jsFiles: 'src/app/scripts/**/*.js',
  jsTestFiles: 'test/spec/**/*.js',
  otherFiles: 'src/app/*.*',
  dist: '../staticfiles/dist/webapp',
  otherDist: '../staticfiles',
  templates: '../server/templates/dist/webapp'
};

gulp.task('styles', () => {
  return gulp.src(config.scssFiles)
    .pipe($.plumber())
    .pipe($.sourcemaps.init())
    .pipe($.sass.sync({
      outputStyle: 'expanded',
      precision: 10,
      includePaths: ['.']
    }).on('error', $.sass.logError))
    .pipe($.autoprefixer({browsers: ['> 1%', 'last 2 versions', 'Firefox ESR']}))
    .pipe($.sourcemaps.write())
    .pipe(gulp.dest('.tmp/app/styles'))
    .pipe(reload({stream: true}));
});

gulp.task('scripts', () => {
  return gulp.src(config.jsFiles)
    .pipe($.plumber())
    .pipe($.sourcemaps.init())
    .pipe($.babel())
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('.tmp/app/scripts'))
    .pipe(reload({stream: true}));
});

function lint(files, options) {
  return () => {
    return gulp.src(files)
      .pipe(reload({stream: true, once: true}))
      .pipe($.eslint(options))
      .pipe($.eslint.format())
      .pipe($.if(!browserSync.active, $.eslint.failAfterError()));
  };
}

const testLintOptions = {
    env: {
        mocha: true
    }
};

const codeLintOptions = {
    rules: {
        "strict": "warning",
        "quotes": "warning"
    },
    globals: {
        'jQuery':false,
        '$':true
    }
};

gulp.task('lint', lint(config.jsFiles, codeLintOptions));
gulp.task('lint:test', lint(config.jsTestFiles, testLintOptions));

gulp.task('html', ['styles', 'scripts'], () => {
  return gulp.src(config.htmlFiles)
    .pipe($.useref({searchPath: ['.tmp', 'src', '.']}))
    .pipe($.if('*.js', $.uglify()))
    .pipe($.if('*.css', $.cssnano()))
    .pipe($.if('*.js', $.rev()))
    .pipe($.if('*.css', $.rev()))
    .pipe($.revReplace())
    .pipe($.if('*.html', $.htmlmin({collapseWhitespace: false})))
    .pipe(gulp.dest(config.dist))
    .pipe($.rev.manifest())
    .pipe(gulp.dest(config.dist));
});

gulp.task('images', () => {
  return gulp.src(config.imageFiles)
    .pipe($.cache($.imagemin({
      progressive: true,
      interlaced: true,
      // don't remove IDs from SVGs, they are often used
      // as hooks for embedding and styling
      svgoPlugins: [{cleanupIDs: false}]
    })))
    .pipe(gulp.dest(config.dist + '/app/images'));
});


gulp.task('fonts', () => {
  return gulp.src(require('npmfiles')('**/*.{eot,svg,ttf,woff,woff2}', function (err) {})
    .concat(config.fontFiles))
    .pipe(gulp.dest('.tmp/app/fonts'))
    .pipe(gulp.dest(config.dist + '/app/fonts'));
});

gulp.task('extras', () => {
  return gulp.src([
    'src/app/*.*'
  ], {
    dot: true
  }).pipe(gulp.dest(config.dist + '/app/extras'));
});

gulp.task('clean', del.bind(null, ['.tmp']));

gulp.task('serve', ['styles', 'scripts', 'fonts'], () => {
  browserSync({
    notify: false,
    port: 9000,
    server: {
      baseDir: ['.tmp', 'src'],
      routes: {
        '/node_modules': 'node_modules'
      }
    }
  });

  gulp.watch([
    config.htmlFiles,
    config.imageFiles,
    '.tmp/app/fonts/**/*'
  ]).on('change', reload);

  gulp.watch(config.scssFiles, ['styles']);
  gulp.watch(config.jsFiles, ['scripts']);
  gulp.watch(config.fontFiles, ['fonts']);
  gulp.watch('package.json', ['wiredep', 'fonts']);
});

gulp.task('serve:dist', () => {
  browserSync({
    notify: false,
    port: 9000,
    server: {
      baseDir: [config.dist]
    }
  });
});

gulp.task('serve:test', ['scripts'], () => {
  browserSync({
    notify: false,
    port: 9000,
    ui: false,
    server: {
      baseDir: 'test',
      routes: {
        '/scripts': '.tmp/app/scripts',
        '/node_modules': 'node_modules'
      }
    }
  });

  gulp.watch(config.jsFiles, ['scripts']);
  gulp.watch(config.jsTestFiles).on('change', reload);
  gulp.watch(config.jsTestFiles, ['lint:test']);
});

// inject NPM components
gulp.task('wiredep', () => {
  gulp.src(config.scssFiles)
    .pipe(wiredep({
      ignorePath: /^(\.\.\/)+/
    }))
    .pipe(gulp.dest('src/app/styles'));

  gulp.src(config.htmlFiles)
    .pipe(wiredep({
      exclude: ['bootstrap-sass'],
      ignorePath: /^(\.\.\/)*\.\./
    }))
    .pipe(gulp.dest('src'));
});

gulp.task('other', () => {
  return gulp.src(config.otherFiles)
    .pipe(gulp.dest(config.otherDist));
});

gulp.task('build', ['lint', 'html', 'images', 'fonts', 'extras'], () => {
  return gulp.src(config.dist + '/**/*').pipe($.size({title: 'build', gzip: true}));
});

gulp.task('templates', ['build'], () => {
  // Black Magic to convert all static references to use django's 'static' templatetags
  return gulp.src(config.dist + '/*.html')
        .pipe(replace(/href="app([/]\S*)"/g, 'href="{% static \'dist/webapp/app$1\' %}"'))
        .pipe(replace(/src="app([/]\S*)"/g, 'src="{% static \'dist/webapp/app$1\' %}"'))
        .pipe(gulp.dest(config.templates));
});

gulp.task('default', ['clean'], () => {
  gulp.start('templates');
});
