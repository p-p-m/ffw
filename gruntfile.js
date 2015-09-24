module.exports = function(grunt) {

    grunt.initConfig({

        sass: {
            dist: {
                options: {
                    style: 'expanded',
                    compass: false
                },
                files: {
                    'assets/css/style.css': 'assets/sass/style.scss'
                }
            }
        },

        autoprefixer: {
            options: {
                browsers: ['last 10 version']
            },
            multiple_files: {
                expand: true,
                flatten: true,
                src: 'assets/css/*.css',
                dest: 'static/css/'
            }
        },

        cssmin: {
            combine: {
                files: {
                    'static/css/style.min.css': ['static/css/style.css']
                }
            }
        },

        concat: {
            dist: {
                src: [
                    'bower_components/jquery/dist/jquery.min.js',
                    'bower_components/jquery-ui/jquery-ui.min.js',
                    'bower_components/jQuery-Mask-Plugin/dist/jquery.mask.min.js',
                    'bower_components/slick.js/slick/slick.js',
                    'bower_components/tooltipster/js/jquery.tooltipster.js',
                    'assets/js/scripts.js'
                ],
                dest: 'static/js/production.js',
            },
            dev: {
                src: [
                    'bower_components/jquery/dist/jquery.min.js',
                    'bower_components/jquery-ui/jquery-ui.min.js',
                    'bower_components/jQuery-Mask-Plugin/dist/jquery.mask.min.js',
                    'bower_components/slick.js/slick/slick.js',
                ],
                dest: 'static/js/dependecies.js',
            }
        },

        uglify: {
            build: {
                src: 'static/js/production.js',
                dest: 'static/js/production.min.js',
            }
        },

        imagemin: {
            dynamic: {
                files: [{
                    expand: true,
                    cwd: 'assets/images/',
                    src: ['**/*.{png,jpg,gif}'],
                    dest: 'static/images/'
                }]
            }
        },

        copy: {
            main: {
                files: [
                    {
                        expand: true,
                        cwd: 'bower_components/fontawesome/css',
                        src: ['*.js'],
                        dest: 'static/css/',
                        filter: 'isFile'
                    },
                    {
                        expand: true,
                        cwd: 'bower_components/normalize.css',
                        src: ['normalize.css'],
                        dest: 'static/css/',
                        filter: 'isFile'
                    },
                    {
                        expand: true,
                        cwd: 'bower_components/fontawesome/fonts',
                        src: ['*'],
                        dest: 'static/fonts/',
                        filter: 'isFile'
                    },
                    {
                        expand: true,
                        cwd: 'bower_components/fontawesome/css',
                        src: ['font-awesome.min.css'],
                        dest: 'static/css/',
                        filter: 'isFile'
                    },
                    {
                        expand: true,
                        cwd: 'bower_components/tooltipster/css',
                        src: ['*/*', 'tooltipster.css'],
                        dest: 'static/css/'
                    }
                ],
            },
        },

        watch: {
            options: {
                livereload: true,
            },
            scripts: {
                files: ['assets/js/*.js'],
                tasks: ['concat'],
                options: {
                    spawn: false,
                }
            },
            css: {
                files: ['assets/sass/*.scss', 'assets/sass/*/*.scss'],
                tasks: ['sass', 'autoprefixer'],
                options: {
                    spawn: false,
                    livereload: false,
                }
            },
            autoprefixer: {
                files: 'assets/css/**',
                tasks: ['autoprefixer']
            },
            images: {
                files: ['assets/images/*.{png,jpg,gif}'],
                tasks: ['imagemin'],
            },
            includereplace: {
                files: ['src/html/*.html', 'src/html/*/*.html'],
                tasks: ['includereplace']
            }
        },

    });

    require('load-grunt-tasks')(grunt);

    grunt.registerTask('build', ['copy', 'concat', 'imagemin', 'sass',
     'autoprefixer', 'uglify', 'cssmin']);
    grunt.registerTask('builddev', ['copy', 'concat:dev', 'imagemin', 'sass',
     'autoprefixer', 'cssmin']);
    grunt.registerTask('run', ['copy', 'concat', 'imagemin',
        'sass', 'autoprefixer', 'uglify', 'cssmin', 'watch']);
    grunt.registerTask('default', ['run']);

};
