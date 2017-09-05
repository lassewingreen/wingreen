<?php 


function enqueue_my_scripts() {
	wp_enqueue_script( 'jquery', '//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js', array('jquery'), '1.9.1', true); // we need the jquery library for Bootstrap js to function
	wp_enqueue_script( 'bootstrap-js', '//netdna.bootstrapcdn.com/bootstrap/3.0.0/js/bootstrap.min.js', array('jquery'), true); // all the bootstrap JavaScript goodness
	}
	add_action('wp_enqueue_scripts', 'enqueue_my_scripts');
	function enqueue_my_styles() {
	wp_enqueue_style( 'bootstrap', '//netdna.bootstrapcdn.com/bootstrap/3.0.0/css/bootstrap.min.css' );
	wp_enqueue_style( 'my-style', get_template_directory_uri() . '/style.css');
	}

	// Add theme support for Custom Logo.
	add_theme_support( 'custom-logo', array(
		'width'       =>"",
		'height'      =>"",
		'flex-height'=>true,
	    'flex-width'=>true,
		
	) );


	 
	 function my_theme_enqueue_styles() { 
 		  wp_enqueue_style( 'parent-style', get_template_directory_uri() . '/style.css' ); 
 		  } 
 
 add_action( 'wp_enqueue_scripts', 'my_theme_enqueue_styles' );

 function cc_mime_types($mimes) {
  $mimes['svg'] = 'image/svg+xml';
  return $mimes;
}
add_filter('upload_mimes', 'cc_mime_types');

function debug_to_console( $data ) {
	if ( is_array( $data ) )
	 $output = "<script>console.log( 'Debug Objects: " . implode( ',', $data) . "' );</script>";
	 else
	 $output = "<script>console.log( 'Debug Objects: " . $data . "' );</script>";
	echo $output;
	}

function custom_scripts() {
	
	wp_register_script( 'custom-script', get_stylesheet_directory_uri() . '/open_burger.js', array() , false, true );
	
	wp_enqueue_script( 'custom-script' );

	//debug_to_console( "Test" );
	
	}
	
	add_action( 'wp_enqueue_scripts', 'custom_scripts', 99 );




?>