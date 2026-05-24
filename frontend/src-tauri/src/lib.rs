mod sidecar;

use sidecar::{SidecarState, start_sidecar};
use std::sync::Mutex;
use tauri::Manager;

#[tauri::command]
fn get_sidecar_port(state: tauri::State<'_, SidecarState>) -> u16 {
    *state.port.lock().unwrap()
}

#[cfg_attr(mobile, tauri::mobile_entry_point)]
pub fn run() {
  tauri::Builder::default()
    .manage(SidecarState {
        child: Mutex::new(None),
        port: Mutex::new(8000),
    })
    .plugin(tauri_plugin_shell::init())
    .setup(|app| {
      if cfg!(debug_assertions) {
        app.handle().plugin(
          tauri_plugin_log::Builder::default()
            .level(log::LevelFilter::Info)
            .build(),
        )?;
      }
      
      if let Err(e) = start_sidecar(app) {
          eprintln!("Failed to start sidecar: {}", e);
      }
      
      Ok(())
    })
    .invoke_handler(tauri::generate_handler![get_sidecar_port])
    .on_window_event(|window, event| {
        if let tauri::WindowEvent::Destroyed = event {
            let app = window.app_handle();
            let state = app.state::<SidecarState>();
            if let Some(child) = state.child.lock().unwrap().take() {
                let _ = child.kill();
                println!("FastAPI Sidecar terminated gracefully.");
            }
        }
    })
    .run(tauri::generate_context!())
    .expect("error while running tauri application");
}
