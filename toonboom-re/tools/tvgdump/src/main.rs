//! tvgdump: parse Toon Boom Harmony .tvg files (format versions 1008 and
//! 1009) and print each parse as one line of JSON: {"file":..., "ok":bool,
//! "data": <FileData[]> | "error": "..."}.
//! Built on the MIT-licensed `tvg` crate by c-probably (github.com/c-probably),
//! forked in ../tvg1008 with added support for the v1008 layout.
use std::io::Cursor;

fn main() {
    let args: Vec<String> = std::env::args().skip(1).collect();
    if args.is_empty() {
        eprintln!("usage: tvgdump <file.tvg> [more.tvg ...]");
        std::process::exit(2);
    }
    // A parser panic on one file must not kill the whole batch.
    std::panic::set_hook(Box::new(|_| {}));
    for path in &args {
        let out = match std::fs::read(path) {
            Ok(bytes) => match std::panic::catch_unwind(|| tvg::read::read(Cursor::new(bytes))) {
                Ok(Ok(data)) => serde_json::json!({"file": path, "ok": true, "data": data}),
                Ok(Err(e)) => serde_json::json!({"file": path, "ok": false, "error": e.to_string()}),
                Err(_) => serde_json::json!({"file": path, "ok": false, "error": "parser panic (caught)"}),
            },

            Err(e) => serde_json::json!({"file": path, "ok": false, "error": e.to_string()}),
        };
        println!("{}", out);
    }
}
