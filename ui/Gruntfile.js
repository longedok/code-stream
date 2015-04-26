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
                files: 'src/css/**/*.css',
                tasks: ['concat:css']
            }
        },

        concat: {
            vendors: {
                src: [
                    'bower_components/jquery/dist/jquery.js',
                    'bower_components/bootstrap/dist/js/bootstrap.js',
                    'bower_components/angular/angular.js',
                    'bower_components/angular-sanitize/angular-sanitize.js',
                    'bower_components/angular-resource/angular-resource.js',
                    'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',
                ],
                dest: 'public/vendors.js'
            },

            app: {
                src: [
                    'src/js/app.js',
                    'public/templates.js'
                ],
                dest: 'public/app.js'
            },

            css: {
                src: [
                    'bower_components/bootstrap/dist/css/bootstrap.css',
                    'src/css/*.css'
                ],
                dest: 'public/style.css'
            }
        },

        ngtemplates: {
            CodeStream: {
                src: ['src/js/templates/**/*.html'],
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
            bootstrap: {
                src: 'bower_components/bootstrap/dist/css/bootstrap.css.map',
                dest: 'public/bootstrap.css.map'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-contrib-symlink');
    grunt.loadNpmTasks('grunt-angular-templates');

    grunt.registerTask('development', ['ngtemplates', 'concat', 'symlink', 'watch']);
    grunt.registerTask('production', ['ngtemplates', 'concat', 'symlink', 'uglify']);
};