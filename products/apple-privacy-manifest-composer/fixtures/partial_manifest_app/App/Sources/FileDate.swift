import Foundation

func readDefaults() -> Bool {
    UserDefaults.standard.bool(forKey: "has-seen-tour")
}

func modifiedAt(url: URL) throws -> Date? {
    try url.resourceValues(forKeys: [.contentModificationDateKey])
        .contentModificationDate
}
