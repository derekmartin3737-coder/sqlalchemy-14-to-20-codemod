from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class ApiPattern:
    category: str
    symbol: str
    pattern: re.Pattern[str]
    confidence: float


REQUIRED_REASON_PATTERNS: tuple[ApiPattern, ...] = (
    ApiPattern(
        "NSPrivacyAccessedAPICategoryUserDefaults",
        "UserDefaults",
        re.compile(r"\b(?:UserDefaults|NSUserDefaults|CFPreferences)\b"),
        0.94,
    ),
    ApiPattern(
        "NSPrivacyAccessedAPICategoryFileTimestamp",
        "file timestamp API",
        re.compile(
            r"\b(?:creationDate|modificationDate|fileModificationDate|"
            r"contentModificationDateKey|creationDateKey|stat|lstat|fstat|"
            r"fstatat|getattrlist|getattrlistbulk|fgetattrlist|getattrlistat)\s*(?:\(|\b)"
        ),
        0.86,
    ),
    ApiPattern(
        "NSPrivacyAccessedAPICategoryDiskSpace",
        "disk space API",
        re.compile(
            r"\b(?:volumeAvailableCapacityKey|"
            r"volumeAvailableCapacityForImportantUsageKey|"
            r"volumeAvailableCapacityForOpportunisticUsageKey|systemFreeSize|"
            r"systemSize|statfs|fstatfs)\s*(?:\(|\b)"
        ),
        0.84,
    ),
    ApiPattern(
        "NSPrivacyAccessedAPICategorySystemBootTime",
        "system boot time API",
        re.compile(
            r"\b(?:systemUptime|mach_absolute_time|mach_continuous_time)\s*(?:\(|\b)"
        ),
        0.86,
    ),
    ApiPattern(
        "NSPrivacyAccessedAPICategoryActiveKeyboards",
        "active keyboard API",
        re.compile(r"\b(?:activeInputModes|UITextInputMode\.activeInputModes)\b"),
        0.9,
    ),
)


LISTED_THIRD_PARTY_SDKS = {
    "abseil",
    "afnetworking",
    "alamofire",
    "appauth",
    "boringssl",
    "capacitor",
    "charts",
    "connectivity_plus",
    "cordova",
    "device_info_plus",
    "firebaseabtesting",
    "firebaseauth",
    "firebasecore",
    "firebasecrashlytics",
    "firebasefirestore",
    "firebasemessaging",
    "flutter",
    "fmdb",
    "googlesignin",
    "googleutilities",
    "grpcpp",
    "hermes",
    "image_picker_ios",
    "kingfisher",
    "lottie",
    "onesignal",
    "openssl",
    "package_info",
    "path_provider",
    "realmswift",
    "rxcocoa",
    "rxswift",
    "sdwebimage",
    "share_plus",
    "snapkit",
    "sqflite",
    "starscream",
    "swiftyjson",
    "toast",
    "unityframework",
    "url_launcher",
    "video_player_avfoundation",
    "wakelock",
    "webview_flutter_wkwebview",
}


DEPENDENCY_FILE_NAMES = {
    "podfile",
    "podfile.lock",
    "package.swift",
    "cartfile",
    "cartfile.resolved",
    "pubspec.yaml",
    "pubspec.lock",
    "package.json",
}
