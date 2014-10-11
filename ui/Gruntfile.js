module.exports = function(grunt) {
    grunt.initConfig({
       pkg: grunt.file.readJSON('package.json'),

       watch: {
           options: {
               livereload: true,
               spawn: false
           },
           files: ['src/**/*'],
           tasks: ['concat']
       },

       concat: {
           application: {
               src: [
                   'src/js/app.js'
               ],
               dest: 'public/app.js'
           },

           css: {
               src: [
                   'bower_components/bootstrap/dist/css/bootstrap.css',
                   'src/css/style.css'
               ],
               dest: 'public/style.css'
           }
       }
    });

    grunt.loadNpmTasks('grunt-contrib-concat');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('dev', ['concat', 'watch']);
    grunt.registerTask('default', ['dev']);
};
