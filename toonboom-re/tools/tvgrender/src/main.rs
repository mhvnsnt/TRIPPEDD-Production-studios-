//! tvgrender: rasterize an SVG file to PNG at a requested pixel width.
//! Usage: tvgrender <in.svg> <out.png> [width_px]
use std::io::Read;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.len() < 2 {
        eprintln!("usage: tvgrender <in.svg> <out.png> [width_px]");
        std::process::exit(2);
    }
    let mut svg = String::new();
    std::fs::File::open(&args[0])
        .and_then(|mut f| f.read_to_string(&mut svg))
        .expect("read svg");
    let tree = usvg::Tree::from_str(&svg, &usvg::Options::default()).expect("parse svg");
    let size = tree.size();
    let target_w = args
        .get(2)
        .and_then(|s| s.parse::<f32>().ok())
        .unwrap_or(1024.0);
    let scale = target_w / size.width();
    let w = (size.width() * scale).ceil() as u32;
    let h = (size.height() * scale).ceil() as u32;
    let mut pixmap = tiny_skia::Pixmap::new(w, h).expect("pixmap");
    resvg::render(
        &tree,
        tiny_skia::Transform::from_scale(scale, scale),
        &mut pixmap.as_mut(),
    );
    pixmap.save_png(&args[1]).expect("save png");
    println!("{}x{}", w, h);
}
