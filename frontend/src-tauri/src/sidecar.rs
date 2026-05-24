use std::net::TcpListener;
use std::sync::Mutex;
use tauri::Manager;
use tauri_plugin_shell::ShellExt;
use tauri_plugin_shell::process::CommandChild;

pub struct SidecarState {
    pub child: Mutex<Option<CommandChild>>,
    pub port: Mutex<u16>,
}

pub fn get_free_port() -> u16 {
    TcpListener::bind("127.0.0.1:0")
        .and_then(|listener| listener.local_addr())
        .map(|addr| addr.port())
        .unwrap_or(8000)
}

pub fn start_sidecar(app: &tauri::App) -> Result<u16, String> {
    let port = get_free_port();
    
    // Store port in state
    let state = app.state::<SidecarState>();
    *state.port.lock().unwrap() = port;
    
    let shell = app.shell();
    let (mut _rx, child) = shell
        .sidecar("app")
        .map_err(|e| format!("Failed to get sidecar: {}", e))?
        .args(&[port.to_string()])
        .spawn()
        .map_err(|e| format!("Failed to spawn sidecar: {}", e))?;
        
    let mut child_guard = state.child.lock().unwrap();
    *child_guard = Some(child);
    
    println!("FastAPI Sidecar successfully spawned on port {}", port);
    Ok(port)
}
