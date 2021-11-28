/**
 * Gulpfile used to build static CSS/JS/Images used by django templates
 */

var gulp = require('gulp');
var chug = require( 'gulp-chug' );
var del = require('del');
var rename = require('gulp-rename');

gulp.paths = {
    src: {
        base: './webapp'
    },
    statics: './staticfiles',
    dist: './staticfiles/dist',
    templates: 'server/templates/dist'
};

gulp.task('clean', function(cb) {
    return del([gulp.paths.dist + '/*'], cb)
});

gulp.task( 'base', ['clean'], function () {
    return gulp.src( gulp.paths.src.base +'/gulpfile.babel.js', { read: false } )
        .pipe( chug({
            tasks:  [  ]
        }) )
});

gulp.task('deploy', ['base'], function () {
    return gulp.src([gulp.paths.statics + '/**', '!'+ gulp.paths.dist + '/**/index.html'])
        .pipe(rename(function (path) {
            path.dirname = 'static/' + path.dirname;
        }))
});

gulp.task('default', ['base']);

