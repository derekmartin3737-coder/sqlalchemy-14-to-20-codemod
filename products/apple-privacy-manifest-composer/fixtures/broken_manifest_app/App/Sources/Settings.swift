import Foundation

func settingsFlag() -> Bool {
    UserDefaults.standard.bool(forKey: "flag")
}
