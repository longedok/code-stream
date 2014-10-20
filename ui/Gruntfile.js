module.exports = function(grunt) {
    grunt.initConfig({
       pkg: grunt.file.readJSON('package.json'),

       watch: {
           options: {
               livereload: true,
               spawn: false
           },
           files: [
               'src/**/*',
               'Gruntfile.js'
           ],
           tasks: ['ngtemplates', 'concat']
       },

       concat: {
           app: {
               src: [
                   'bower_components/jquery/dist/jquery.js',
                   'bower_components/angular/angular.js',
                   'bower_components/angular-sanitize/angular-sanitize.js',
                   'bower_components/angular-resource/angular-resource.js',
                   'bower_components/angular-bootstrap/ui-bootstrap-tpls.js',

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
               src: ['src/js/templates/**.html', 'src/js/templates/**/**.html'],
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
       }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');
    grunt.loadNpmTasks('grunt-contrib-uglify');
    grunt.loadNpmTasks('grunt-angular-templates');

    grunt.registerTask('dev', ['ngtemplates', 'concat', 'watch']);
    grunt.registerTask('prod', ['ngtemplates', 'concat', 'uglify']);
    grunt.registerTask('default', ['dev']);
};