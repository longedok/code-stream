module.exports = function(grunt) {
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        watch: {
            options: {
                livereload: true,
                spawn: false
            },

            js: {
                files: [
                    'src/js/**/*.js',
                    'Gruntfile.js'
                ],
                tasks: ['concat:app']
            },

            html: {
                files: [
                    'src/js/**/*.html'
                ],
                tasks: ['ngtemplates', 'concat:app']
            },

            css: {
                files: 'src/sass/**/*.scss',
                tasks: ['sass']
            }
        },

        sass: {
            options: {
                includePaths: [
                    'bower_components/fontawesome/scss',
                    'bower_components/bootstrap-sass/assets/stylesheets'
                ]
            },
            main: {
                src: 'src/sass/main.scss',
                dest: 'public/style.css'
            }
        },

        concat: {
            vendors: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/bootstrap-sass/assets/javascripts/bootstrap.js',
                    'bower_components/angular/angular.js',
                    'bower_components/angular-sanitize/angular-sanitize.js',
                    'bower_components/angular-resource/angular-resource.js',
                    'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
                    'bower_components/moment/moment.js',
                    'bower_components/angular-moment/angular-moment.js'
                ],
                dest: 'public/vendors.js'
            },

            app: {
                src: [
                    'src/js/app.js',
                    'src/js/**/*.js',
                    'public/templates.js'
                ],
                dest: 'public/app.js'
            }
        },

        ngtemplates: {
            CodeStream: {
                cwd: 'src/js',
                src: ['templates/**/*.html'],
                dest: 'public/templates.js'
            }
        },

        uglify: {
            js: {
                src: [
                    'public/app.js'
                ],
                dest: 'public/app.js'
            }
        },

        symlink: {
            main: {
                src: 'src/fonts',
                dest: 'public/fonts/main'
            },
            fa: {
                src: 'bower_components/fontawesome/fonts',
                dest: 'public/fonts/fontawesome'
            },
            glyphicons: {
                src: 'bower_components/bootstrap-sass/assets/fonts/bootstrap',
                dest: 'public/fonts/bootstrap'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-symlink');
    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-angular-templates');

    grunt.registerTask('development', ['ngtemplates', 'sass', 'concat', 'symlink', 'watch']);
    grunt.registerTask('production', ['ngtemplates', 'sass', 'concat', 'symlink', 'uglify']);
};