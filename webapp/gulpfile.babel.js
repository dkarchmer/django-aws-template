// generated on 2016-03-23 using generator-webapp 2.0.0
import gulp from 'gulp';
import del from 'del';
import {stream as wiredep} from 'wiredep';
import replace from 'gulp-replace';
var gulpLoadPlugins = require('gulp-load-plugins');

const $ = gulpLoadPlugins();

const config = {
  htmlFiles: 'src/*.html',
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
    .pipe(gulp.dest('.tmp/app/styles'));
});

gulp.task('scripts', () => {
  return gulp.src(config.jsFiles)
    .pipe($.plumber())
    .pipe($.sourcemaps.init())
    .pipe($.babel())
    .pipe($.sourcemaps.write('.'))
    .pipe(gulp.dest('.tmp/app/scripts'));
});

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

gulp.task('build', ['html', 'fonts', 'extras'], () => {
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
